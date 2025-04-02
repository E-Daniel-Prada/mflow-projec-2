
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from fetch_data import fetch_data
from preprocess import preprocess_data
from feature_engineering import feature_engineering
from train_model import train_model
from register_model import register_model

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'mlops_pipeline',
    default_args=default_args,
    description='Pipeline de MLOps con Airflow y MLflow',
    schedule_interval=timedelta(minutes=5),
    catchup=False
)

task_fetch = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag
)

task_preprocess = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

task_feature_eng = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering,
    dag=dag
)

task_train = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

task_register = PythonOperator(
    task_id='register_model',
    python_callable=register_model,
    dag=dag
)

task_fetch >> task_preprocess >> task_feature_eng >> task_train >> task_register
