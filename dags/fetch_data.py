import requests
import pandas as pd
from airflow.models import Variable
from sqlalchemy import create_engine
import pymysql
import requests
import json

# Nombre de la variable en Airflow
ID_VARIABLE_NAME = "current_api_id"

# Inicializar variable si no existe
if not Variable.get(ID_VARIABLE_NAME, default_var=None):
    Variable.set(ID_VARIABLE_NAME, 1)  # Comienza en 1

# Función para obtener el ID y actualizarlo
def get_next_id():
    current_id = int(Variable.get(ID_VARIABLE_NAME, default_var=1))  # Obtener el ID actual
    next_id = current_id + 1 if current_id < 10 else 1  # Reiniciar en 1 después de 10
    Variable.set(ID_VARIABLE_NAME, next_id)  # Guardar nuevo ID en Airflow
    return current_id  # Retornar el ID actual para la ejecución


# Función para extraer datos desde la API
def fetch_data(**kwargs):
    batch_id = get_next_id()
    url = f"http://192.168.1.14:80/data?group_number={batch_id}"
    
    response = requests.get(url)
    data = response.json()
    
    records = data.get("data", [])
    return records

# Función para insertar datos en MySQL
def insert_data(**kwargs):
    ti = kwargs['ti']
    records = ti.xcom_pull(task_ids='fetch_data')
    
    conn = pymysql.connect(
        host="mysql_host",
        user="data_user",
        password="data_pass",
        database="data_db"
    )
    
    cursor = conn.cursor()

    table_name = "dataset_table"
    columns = [f"col{i}" for i in range(1, 54)]

    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    
    cursor.executemany(query, records)
    
    conn.commit()
    cursor.close()
    conn.close()