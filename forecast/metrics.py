"""
Forecast evaluation metrics.
"""

from sklearn.metrics import (mean_absolute_error,mean_squared_error,)
import numpy as np


def evaluate_forecast(actual,predicted,) -> dict:
    """
    Calculate forecasting metrics.

    Args:
        actual:
            Ground truth values.

        predicted:
            Forecast values.

    Returns:
        Dictionary containing evaluation metrics.
    """

    mae = mean_absolute_error(actual,predicted,)

    rmse = np.sqrt(mean_squared_error(actual,predicted,))

    mape = np.mean(np.abs((actual - predicted)/ actual)) * 100

    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2),
    }