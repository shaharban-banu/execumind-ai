import pandas as pd
from pathlib import Path

RAW_PATH="data/raw"
PROCESSED_PATH="data/processed"

Path(PROCESSED_PATH).mkdir(parents=True,exist_ok=True)

def transform_customers():
    df=pd.read_csv(f"{RAW_PATH}/olist_customers_dataset.csv")
    print("customer before :",df.shape)
    df=df.drop_duplicates()
    df['']
