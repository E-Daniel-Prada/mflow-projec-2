import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def feature_engineering():
    engine = create_engine('mysql+pymysql://data_user:data_pass@mysql/data_db')
    df = pd.read_sql('SELECT * FROM cleaned_data', engine)

    df['log_value'] = df['value'].apply(lambda x: np.log1p(x))

    df.to_sql('processed_data', engine, if_exists='replace', index=False)
    print("Características extraídas y almacenadas en MySQL")
