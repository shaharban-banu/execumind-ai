"""
Train Revenue Forecast Model.

Aggregates historical monthly revenue from the
Olist dataset and trains a Prophet forecasting model.
"""
import pandas as pd
from database.database import engine
from utils.logger import logger
import joblib
from pathlib import Path
from prophet import Prophet
from forecast.forecasting import load_time_series

MODEL_DIR=Path("forecast/models")
MODEL_DIR.mkdir(parents=True,exist_ok=True)


METRICES=[
    "revenue",
    "orders",
    "customers",
    "aov",]

def train_metric(metric):
    """
    Train Prophet model.

    Returns
    -------
    Prophet
        Trained model.
    """
    logger.info("Training Prophet model %s",metric)
    df=load_time_series(metric)
   
    print(df.shape)
    model=Prophet(yearly_seasonality=False,
                  weekly_seasonality=False,
                  daily_seasonality=False,
                  n_changepoints=5,
                  changepoint_prior_scale=0.05,)
    model.fit(df)
    MODEL_PATH=MODEL_DIR/f"{metric}.pkl"
    joblib.dump(model,MODEL_PATH)
    logger.info("%s Model saved to %s",metric,MODEL_PATH)

def train_all():
    logger.info("Starting forecast model training")
    for metric in METRICES:
        train_metric(metric)
    logger.info("All forecast models trained successfully")

if __name__=="__main__":
    train_all()