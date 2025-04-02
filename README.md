# mlflow-project-2

# Proyecto de Ingesta y Procesamiento de Datos

## Descripción
Este proyecto tiene como objetivo la ingesta, procesamiento y almacenamiento de bloques de información desde una API externa a una base de datos MySQL. La información es obtenida en lotes a través de una tarea automatizada en Apache Airflow, que consulta la API cada 5 minutos y almacena los datos en la base de datos.

## Tecnologías Utilizadas
- **Docker**: Para la contenedorización de los servicios.
- **Docker Compose**: Para la orquestación de múltiples contenedores.
- **Apache Airflow**: Para la orquestación de tareas de ingesta de datos.
- **MySQL**: Para el almacenamiento de los datos procesados.
- **Python**: Para la implementación de los scripts de procesamiento.

## Estructura del Proyecto
```
mlflow-project-2/
│── dags/                        # DAGs de Airflow
│   ├── fetch_data.py            # Descarga datos desde API externa
│   ├── preprocess.py            # Limpieza y normalización
│   ├── feature_engineering.py    # Preprocesamiento de datos
│   ├── train_model.py            # Entrenamiento del modelo
│   ├── register_model.py         # Registro del modelo en MLflow
│   ├── main_dag.py               # DAG principal
│── docker-compose.yml            # Orquestación de servicios
│── Dockerfile                    # Imagen para Airflow
│── requirements.txt               # Librerías necesarias
│── mlflow/                        # Archivos de configuración MLflow
│── scripts/                       # Scripts auxiliares
│── notebooks/                     # Jupyter Notebooks opcionales
```

## Instalación y Configuración
### 1. Clonar el repositorio
```sh
git clone git@github.com:E-Daniel-Prada/mlflow-project-2.git
cd mlflow-project-2
```

### 2. Levantar los Servicios

```sh
docker-compose up -d
```

### 3. Acceder a los Servicios
- **Airflow Web UI**: `http://localhost:8082`
- **API Externa**: `http://localhost:80/data?group_number=1`
- **MLFLOW**: `http://localhost:5000/`
- **MySQL**: `mysql://usuario:contraseña@localhost:3306/database`

## Flujo de Trabajo
1. **Apache Airflow** ejecuta la tarea `fetch_data.py` cada 5 minutos.
2. La tarea consulta la API externa en `http://host.docker.internal:80/data?group_number={batch_id}`.
3. Se incrementa `batch_id` en cada ejecución para obtener nuevos bloques de datos.
4. Los datos obtenidos se insertan en la base de datos MySQL.
5. Opcionalmente, `process_data.py` puede realizar transformaciones en los datos.

## Consideraciones
- Si `host.docker.internal` no funciona en Linux, se debe usar la IP del host manualmente.
- Si se necesitan logs en tiempo real de Airflow:
  ```sh
  docker logs -f airflow_scheduler
  ```
- Para verificar la red de Docker:
  ```sh
  docker network ls
  ```