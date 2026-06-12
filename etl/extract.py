import pandas as pd
from config.settings import DATA_DIR

RAW_PATH = DATA_DIR / "raw"


def extract_customers():
    return pd.read_csv(RAW_PATH / "olist_customers_dataset.csv")


def extract_orders():
    return pd.read_csv(RAW_PATH / "olist_orders_dataset.csv")


def extract_products():
    return pd.read_csv(RAW_PATH / "olist_products_dataset.csv")


def extract_reviews():
    return pd.read_csv(RAW_PATH / "olist_order_reviews_dataset.csv")


def extract_sellers():
    return pd.read_csv(RAW_PATH / "olist_sellers_dataset.csv")


def extract_payments():
    return pd.read_csv(RAW_PATH / "olist_order_payments_dataset.csv")


def extract_order_items():
    return pd.read_csv(RAW_PATH / "olist_order_items_dataset.csv")


def extract_geolocation():
    return pd.read_csv(RAW_PATH / "olist_geolocation_dataset.csv")
