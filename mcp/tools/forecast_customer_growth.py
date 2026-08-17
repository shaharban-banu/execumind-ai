"""
Customer Growth Forecast MCP Tool.

Provides forecasting capabilities for customer growth
using the forecasting service.

The Forecast Agent uses this tool instead of interacting
directly with the forecasting model.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_customer_growth(user_id:int,periods:int=6):
    """
    Forecast customer growth.

    Generates future customer growth predictions for the
    specified forecast horizon.

    Args:
        periods: Number of future periods to forecast.

    Returns:
        Forecast result containing predicted customer values.

    Raises:
        RuntimeError: If forecasting fails.
    """
    logger.info("Forecasting customer growth")
    try:
        return _predictor.predict(user_id=user_id,metric='customers',periods=periods)
    except Exception as exc:
        logger.exception(
            "Customer growth forecast failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to forecast customer growth."
        ) from exc