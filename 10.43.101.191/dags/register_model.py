import mlflow
import joblib
import os

def register_model():
    try:
        # Establecer la URI de tracking de MLflow
        #mlflow.set_tracking_uri("http://mlflow:5000")
        mlflow.set_tracking_uri("http://10.43.101.184:5000")

        os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://10.43.101.184:9000"
        os.environ['AWS_ACCESS_KEY_ID'] = 'admin'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'supersecret'

        # Cargar el modelo desde el archivo pickle
        model_path = "/shared/model.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No se encontró el archivo {model_path}")
        
        model = joblib.load(model_path)

        # Iniciar experimento (si no existe, lo crea)
        experiment_name = "forest-cover-type-project2-experiment-register"
        mlflow.set_experiment(experiment_name)

        with mlflow.start_run():
            mlflow.log_param("model_type", "RandomForestClassifier")
            mlflow.sklearn.log_model(model, "model", registered_model_name="RandomForestClassifier-project2")
            mlflow.log_artifact(model_path)

        print("Modelo registrado correctamente en MLflow")

    except Exception as e:
        print(f"[ERROR] Error al registrar el modelo: {str(e)}")
