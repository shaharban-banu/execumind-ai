
"""
Generic forecasting evaluation metrics.

Used to compute MAE, RMSE and MAPE for any forecasting model.
Current Prophet evaluation uses Prophet's built-in rolling
cross-validation and performance_metrics().
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

    actual = np.asarray(actual)
    predicted = np.asarray(predicted)

    mask = actual != 0

    mape = (
        np.mean(
            np.abs((actual[mask] - predicted[mask]) / actual[mask])
        ) * 100
    )

    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2),
    }