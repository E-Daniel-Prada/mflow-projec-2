import requests
from airflow.models import Variable
import requests
import mysql.connector
from mysql.connector import Error
import logging
# Nombre de la variable en Airflow
ID_VARIABLE_NAME = "current_api_id"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Inicializar variable si no existe
if not Variable.get(ID_VARIABLE_NAME, default_var=None):
    Variable.set(ID_VARIABLE_NAME, 4)  # Comienza en 1

# Función para obtener el ID y actualizarlo
def get_next_id():
    current_id = int(Variable.get(ID_VARIABLE_NAME, default_var=1))  # Obtener el ID actual
    next_id = current_id + 1 if current_id < 10 else 1  # Reiniciar en 1 después de 10
    Variable.set(ID_VARIABLE_NAME, next_id)  # Guardar nuevo ID en Airflow
    return current_id  # Retornar el ID actual para la ejecución


# Función para extraer datos desde la API
def fetch_data(**kwargs):
    batch_id = get_next_id()
    #url = f"http://192.168.1.14:80/data?group_number={batch_id}"
    url = f"http://10.43.101.191:80/data?group_number={batch_id}"
    try:
        response = requests.get(url)
        data = response.json()
        
        records = data.get("data", [])
        if records:
            insert_records_to_mysql(records)
            logger.info(f"Batch {batch_id}: {len(records)} records fetched and inserted.")
        else:
           logger.info(f"Batch {batch_id}: No data found.")
    except Exception as e:
        logger.error(f"Failed to fetch or insert batch {batch_id}: {e}")

# Función para insertar datos en MySQL
def insert_records_to_mysql(records):
    try:
        connection = mysql.connector.connect(
            host='mysql',
            user='root',
            password='root',
            database='data_db'
        )

        columns = [
            "elevation", "aspect", "slope", 
            "horizontal_distance_to_hydrology",
            "vertical_distance_to_hydrology",
            "Horizontal_Distance_To_Roadways",
            "Hillshade_9am",
            "Hillshade_Noon",
            "Hillshade_3pm",
            "Horizontal_Distance_To_Fire_Points",
            "Wilderness_Area1", "Wilderness_Area2", "Wilderness_Area3", "Wilderness_Area4",
            *[f"Soil_Type{i}" for i in range(1, 41)],
            "Cover_Typ"
        ]

        insert_query = f"""
            INSERT INTO forest_data ({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))})
        """
        values = [tuple(record) for record in records]

        # DEBUG: imprimir la query de ejemplo formateada con el primer registro
        example_values = values[0]
        formatted_query = insert_query.replace("%s", "'{}'")
        logger.info("Ejemplo de query con valores reales:")
        logger.info(formatted_query.format(*example_values))
        
        
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE cleaned_data")
            cursor.executemany(insert_query, values)
            connection.commit()
            logger.info(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        logger.error(e)
        print("Error inserting records:", e)