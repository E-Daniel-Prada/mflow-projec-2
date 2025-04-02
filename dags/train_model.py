import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

def train_model():
    engine = create_engine('mysql+pymysql://data_user:data_pass@mysql/data_db')
    df = pd.read_sql('SELECT * FROM processed_data', engine)

    X = df[['log_value']]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    joblib.dump(model, "model.pkl")
    mlflow.sklearn.log_model(model, "model")

    print("Modelo entrenado y guardado")
