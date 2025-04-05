import mlflow
from mlflow.tracking import MlflowClient

# Configura el URI del servidor MLflow
mlflow.set_tracking_uri("http://10.43.101.184:5000")

# Cliente para interactuar con MLflow
client = MlflowClient()

# Datos del run que ya tiene el modelo logueado
run_id = "ba09dedb82554c84afed58b0bbc483d5"
artifact_path = "sklearn"  # El nombre bajo "Logged models" en la UI

# Ruta completa al modelo
model_uri = f"runs:/{run_id}/{artifact_path}"

# Nombre que le vas a dar al nuevo modelo registrado
new_model_name = "grid_search_v2_prueba"

# Registro del modelo
try:
    result = mlflow.register_model(model_uri=model_uri, name=new_model_name)
    print(f"✅ Modelo registrado exitosamente: {result.name}, versión {result.version}")
except Exception as e:
    print(f"❌ Error registrando modelo: {e}")
