"""
Order Forecast MCP Tool.

Provides forecasting capabilities for future order volume
using the forecasting service.

The Forecast Agent uses this tool instead of interacting
directly with the forecasting model.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_orders(periods:int=6):
    """
    Forecast future order volume.

    Generates order forecasts for the specified
    forecast horizon.

    Args:
        periods: Number of future periods to forecast.

    Returns:
        Forecast result containing predicted order values.

    Raises:
        RuntimeError: If forecasting fails.
    """
    logger.info("Forecasting orders")

    try:
        return _predictor.predict(metric='orders',periods=periods)
    except Exception as exc:
        logger.exception(
            "Order forecast failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to forecast orders."
        ) from exc