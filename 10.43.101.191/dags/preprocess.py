import mysql.connector
from airflow.decorators import task
import logging

logger = logging.getLogger(__name__)

# Lista de campos numéricos que se van a normalizar
NUMERIC_FIELDS = [
    "elevation", "aspect", "slope", 
    "horizontal_distance_to_hydrology",
    "vertical_distance_to_hydrology",
    "Horizontal_Distance_To_Roadways",
    "Hillshade_9am",
    "Hillshade_Noon",
    "Hillshade_3pm",
    "Horizontal_Distance_To_Fire_Points"
]

def min_max_scale(x, min_val, max_val):
    if max_val - min_val == 0:
        return 0
    return (x - min_val) / (max_val - min_val)

def preprocess_data(**kwargs):
    try:
        connection = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root",
            database="data_db"
        )
        logger.info(f"estoy aqui *************")
        with connection.cursor() as cursor:
            # Leer datos de la tabla original
            cursor.execute("SELECT * FROM forest_data")
            rows = cursor.fetchall()

            # Obtener nombres de columnas
            col_names = [desc[0] for desc in cursor.description]
            col_indices = {name: i for i, name in enumerate(col_names)}

            logger.info(f"Se leyeron {len(rows)} filas.")

            # Inicializar min y max para cada campo numérico
            mins = {col: float('inf') for col in NUMERIC_FIELDS}
            maxs = {col: float('-inf') for col in NUMERIC_FIELDS}

            # Calcular min y max
            for row in rows:
                for col in NUMERIC_FIELDS:
                    val = row[col_indices[col]]
                    try:
                        val = float(val)
                        if val < mins[col]: mins[col] = val
                        if val > maxs[col]: maxs[col] = val
                    except (ValueError, TypeError):
                        logger.warning(f"Valor inválido en columna {col}: {val}")
                        continue

            logger.info(f"Minimos: {mins}")
            logger.info(f"Maximos: {maxs}")

            # Truncar la tabla cleaned_data
            cursor.execute("TRUNCATE TABLE cleaned_data")

            # Normalizar e insertar datos procesados
            processed_data = []
            for row in rows:
                row = list(row)
                for col in NUMERIC_FIELDS:
                    idx = col_indices[col]
                    try:
                        row[idx] = min_max_scale(float(row[idx]), mins[col], maxs[col])
                    except (ValueError, TypeError):
                        logger.warning(f"No se pudo normalizar {col} con valor {row[idx]}")
                        row[idx] = 0
                processed_data.append(tuple(row))

            placeholders = ", ".join(["%s"] * len(col_names))
            columns = ", ".join(col_names)
            query = f"INSERT INTO cleaned_data ({columns}) VALUES ({placeholders})"

            logger.info(f"Ejecutando query: {query}")

            cursor.executemany(query, processed_data)
            connection.commit()
            logger.info(f"Se insertaron {cursor.rowcount} filas en cleaned_data.")

    except Exception as e:
        logger.error(f"Error en preprocesamiento: {e}")

    finally:
        if connection.is_connected():
            connection.close()
    return None 