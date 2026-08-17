"""
Average Order Value Forecast MCP Tool.

Provides forecasting capabilities for Average Order Value (AOV)
using the forecasting service.

The Forecast Agent uses this tool instead of interacting
directly with the forecasting model.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_average_order_value(user_id:int,periods:int=6):
    """
    Forecast Average Order Value (AOV).

    Generates future AOV predictions for the specified
    forecast horizon.

    Args:
        periods: Number of future periods to forecast.

    Returns:
        Forecast result containing predicted AOV values.

    Raises:
        RuntimeError: If forecasting fails.
    """
    logger.info("Forecasting average  order value")
    try:
        return _predictor.predict(user_id=user_id,metric='aov',periods=periods)
    except Exception as exc:
        logger.exception(
            "Average order value forecast failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to forecast average order value."
        ) from exc