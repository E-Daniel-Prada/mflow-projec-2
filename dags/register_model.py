import mlflow
import mlflow.sklearn
import os

def register_model():
    try:
        mlflow.set_tracking_uri("http://mlflow:5000")
        mlflow.set_experiment("forest-cover-type")

        # Iniciar una nueva ejecución
        with mlflow.start_run(run_name="model_register"):

            # Registrar el modelo entrenado previamente
            model_path = "model.pkl"
            if not os.path.exists(model_path):
                raise FileNotFoundError("No se encontró model.pkl para registrar")

            # Cargar y registrar el modelo con un nombre explícito
            model = mlflow.sklearn.load_model(model_path)
            mlflow.sklearn.log_model(model, "model", registered_model_name="RandomForestCoverType")

            print("Modelo registrado en MLflow")

    except Exception as e:
        print(f"[ERROR] Error al registrar el modelo: {e}")
