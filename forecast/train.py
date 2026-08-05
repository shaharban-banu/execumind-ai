"""
Train Revenue Forecast Model.

Aggregates historical monthly revenue from the
Olist dataset and trains a Prophet forecasting model.
"""
import pandas as pd
from utils.logger import logger
import joblib
from pathlib import Path
from prophet import Prophet
from forecast.forecasting import load_time_series

MODEL_DIR=Path("data/models")
MODEL_DIR.mkdir(parents=True,exist_ok=True)


METRICES=[
    "revenue",
    "orders",
    "customers",
    "aov",]

def train_metric(metric):
    """
    Train and save a Prophet forecasting model.

    Loads historical time-series data for the specified metric,
    trains a Prophet model, and stores the trained model on disk.

    Args:
        metric: Forecast metric to train.

    Raises:
        RuntimeError: If model training or saving fails.
    """
    logger.info("Training Prophet model %s",metric)

    try:
        df=load_time_series(metric)
    
        logger.debug("Loaded %d observations for '%s'.",len(df),metric,)

        model=Prophet(yearly_seasonality=False,
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    n_changepoints=5,
                    changepoint_prior_scale=0.05,)
        model.fit(df)
        MODEL_PATH=MODEL_DIR/f"{metric}.pkl"
        joblib.dump(model,MODEL_PATH)
        logger.info("%s Model saved to %s",metric,MODEL_PATH)

    except Exception as exc:
        logger.exception(
            "Failed to train '%s' model: %s",
            metric,
            exc,
        )
        raise RuntimeError(
            f"Model training failed for '{metric}'."
        ) from exc

def train_all():
    """
    Train forecasting models for all supported metrics.

    Iterates through each configured metric, trains a Prophet model,
    and saves the trained model to the models directory.

    Raises:
        RuntimeError: If training any model fails.
    """

    logger.info("Starting forecast model training")

    try:
        for metric in METRICES:
            train_metric(metric)
        logger.info("All forecast models trained successfully")

    except Exception as exc:
        logger.exception(
            "Forecast training failed: %s",
            exc,
        )
        raise

if __name__=="__main__":
    train_all()