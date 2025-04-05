import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

import mlflow
from mlflow.tracking import MlflowClient
from app.inference import (
    load_model_from_minio,
    make_prediction,
    get_experiment_details,
    get_run_details
)

# Cargar variables de entorno desde .env
load_dotenv()

# Crear la app FastAPI
app = FastAPI()

# Inicializar el modelo cargado desde MinIO
model = load_model_from_minio(
    run_id="ba09dedb82554c84afed58b0bbc483d5",  
    artifact_subpath="model",                   
    experiment_id="5"                          
)

# Clase para la entrada del endpoint /predict
class InputData(BaseModel):
    features: list  # Lista de valores para la predicción

@app.get("/")
def home():
    return {"message": "API de Inferencia y Experimentos con MLflow está corriendo"}

@app.post("/predict/")
def predict(data: InputData):
    """Realiza una predicción usando el modelo cargado."""
    return make_prediction(model, [data.features])

@app.get("/experiment/{experiment_name}")
def experiment_info(experiment_name: str):
    """Devuelve información de un experimento en MLflow."""
    return get_experiment_details(experiment_name)

@app.get("/run/{run_id}")
def run_info(run_id: str):
    """Devuelve detalles de un run en MLflow."""
    return get_run_details(run_id)

@app.get("/models")
def list_models():
    """Lista modelos registrados en MLflow Registry (si hay)."""
    try:
        mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "http://10.43.101.184:5000")
        mlflow.set_tracking_uri(mlflow_uri)
        print("🔍 Tracking URI en tiempo real:", mlflow.get_tracking_uri())

        client = MlflowClient()
        models = client.search_registered_models()
        print("🧪 Modelos encontrados:", models)

        if not models:
            print("⚠️ Lista vacía desde FastAPI")
            return {"message": "No hay modelos registrados en MLflow"}
        return {"models": [m.name for m in models]}
    except Exception as e:
        print("❌ Error:", str(e))
        return {"error": str(e)}

@app.get("/load-model-from-minio/{run_id}")
def load_from_minio(run_id: str, artifact_path: str = "model", experiment_id: str = "5"):
    """
    Carga manualmente un modelo desde MinIO usando su run_id.
    """
    global model
    new_model = load_model_from_minio(run_id, artifact_path, experiment_id)
    if new_model is None:
        return {"error": "No se pudo cargar el modelo desde MinIO"}
    model = new_model
    return {"message": f"✅ Modelo cargado desde MinIO (run_id: {run_id}, path: {artifact_path})"}
