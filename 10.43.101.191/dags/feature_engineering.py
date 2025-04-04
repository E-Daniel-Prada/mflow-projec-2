import mysql.connector
import pandas as pd
import numpy as np

def feature_engineering():
    try:
        # Conexión
        connection = mysql.connector.connect(
            host='mysql_data',
            user='data_user',
            password='data_pass',
            database='data_db'
        )

        # Leer los datos preprocesados
        query = "SELECT * FROM cleaned_data"
        df = pd.read_sql(query, connection)

        print(f"[INFO] Se cargaron {len(df)} registros de cleaned_data")

        # Convertir columnas numéricas explícitamente
        columnas_numericas = [
            'elevation', 'aspect', 'slope', 'horizontal_distance_to_hydrology',
            'vertical_distance_to_hydrology', 'Horizontal_Distance_To_Roadways',
            'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
            'Horizontal_Distance_To_Fire_Points'
        ]

        for col in columnas_numericas:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Crear nuevas características
        df['Relative_Slope'] = df['slope'] / (df['elevation'] + 1)

        df['Total_Hydrology_Distance'] = np.sqrt(
            df['horizontal_distance_to_hydrology'] ** 2 +
            df['vertical_distance_to_hydrology'] ** 2
        )

        # Eliminar tabla anterior si existe
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE engineered_data")
            connection.commit()

        # Insertar datos con cursor
        cols = ",".join(df.columns)
        placeholders = ",".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO engineered_data ({cols}) VALUES ({placeholders})"

        data = df.values.tolist()
        with connection.cursor() as cursor:
            cursor.executemany(insert_query, data)
            connection.commit()

        print("[INFO] Inserción en engineered_data completada")

    except Exception as e:
        print(f"[ERROR] Error en feature_engineering: {e}")

    finally:
        if connection.is_connected():
            connection.close()
