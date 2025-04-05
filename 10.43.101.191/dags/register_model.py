import mlflow
import joblib
import os

def register_model():
    try:
        # Establecer la URI de tracking de MLflow
        mlflow.set_tracking_uri("http://10.43.101.184:5000")

        # Cargar el modelo desde el archivo pickle
        model_path = "model.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No se encontró el archivo {model_path}")
        
        model = joblib.load(model_path)

        # Iniciar experimento (si no existe, lo crea)
        experiment_name = "ML Model Experiment"
        mlflow.set_experiment(experiment_name)

        with mlflow.start_run():
            mlflow.log_param("model_type", "Linear Regression")
            mlflow.sklearn.log_model(model, "model", registered_model_name="LinearRegressionCoverType")
            mlflow.log_artifact(model_path)

        print("✅ Modelo registrado correctamente en MLflow")

    except Exception as e:
        print(f"[ERROR] Error al registrar el modelo: {str(e)}")
