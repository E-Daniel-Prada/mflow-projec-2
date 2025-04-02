import mlflow
import os  # ✅ Para manejar rutas
import shutil  # ✅ Para copiar archivos

def register_model():
    mlflow.set_tracking_uri("http://mlflow:5000")

    experiment_id = mlflow.create_experiment("ML Model Experiment")
    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.log_param("model", "Linear Regression")
        mlflow.log_artifact("model.pkl")
    
    print("Modelo registrado en MLflow")
