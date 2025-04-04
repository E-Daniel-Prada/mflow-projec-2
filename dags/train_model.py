import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine

def train_model():
    try:
        engine = create_engine('mysql+pymysql://root:root@mysql/data_db')
        df = pd.read_sql('SELECT * FROM engineered_data', engine)

        # Features y target
        X = df.drop(columns=["Cover_Typ"])  # Cambia esto si tu columna target tiene otro nombre
        y = df["Cover_Typ"]

        # División train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Modelo
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predicción y evaluación
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Accuracy: {accuracy:.4f}")

        # Guardar modelo
        joblib.dump(model, "model.pkl")

        # Registrar con MLflow
        mlflow.set_experiment("forest-cover-type")
        with mlflow.start_run():
            mlflow.sklearn.log_model(model, "model")
            mlflow.log_metric("accuracy", accuracy)

        print("Modelo entrenado, guardado y registrado en MLflow")

    except Exception as e:
        print(f"[ERROR] Error en train_model: {e}")
