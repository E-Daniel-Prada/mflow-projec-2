import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def preprocess_data():
    engine = create_engine('mysql+pymysql://data_user:data_pass@mysql/data_db')
    df = pd.read_sql('SELECT * FROM raw_data', engine)

    df.dropna(inplace=True)
    df = df[df['value'] > 0]

    df.to_sql('cleaned_data', engine, if_exists='replace', index=False)
    print("Datos normalizados y almacenados en MySQL")
