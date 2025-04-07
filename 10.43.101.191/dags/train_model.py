import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def train_model():
    try:
        # Establecer tracking URI
        mlflow.set_tracking_uri("http://mlflow:5000")

        # Cargar datos
        engine = create_engine('mysql+pymysql://root:root@mysql/data_db')
        df = pd.read_sql('SELECT * FROM engineered_data', engine)

        # Features y target
        X = df.drop(columns=["Cover_Typ"])
        y = df["Cover_Typ"]

        # División train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Entrenamiento
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluación
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        logger.info(f"***** Accuracy: {accuracy:.4f} | Precision: {precision:.4f} | Recall: {recall:.4f} | F1: {f1:.4f}")

        # Guardar modelo localmente
        model_path = "/shared/model.pkl"
        joblib.dump(model, "/shared/model.pkl")

        # Iniciar experimento MLflow
        mlflow.set_experiment("forest-cover-type")

        with mlflow.start_run(run_name="RandomForest_Train"):
            # Log de parámetros y métricas
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("random_state", 42)

            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1_score", f1)

            # Log del modelo
            mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name="ForestCoverClassifier")

            # Log del archivo pickle (opcional)
            mlflow.log_artifact(model_path)

        logger.info("✅ Modelo entrenado, guardado y registrado en MLflow")

    except Exception as e:
        logger.info(f"[ERROR] Error en train_model: {e}")
