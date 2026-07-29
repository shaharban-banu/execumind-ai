"""
Revenue Forecast MCP Tool.

Provides revenue forecasting capability
for the Forecast Intelligence Agent.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_revenue(periods:int=6):
    """
    Forecast future revenue.

    Generates revenue forecasts for the specified
    forecast horizon.

    Args:
        periods: Number of future periods to forecast.

    Returns:
        Forecast result containing predicted revenue values.

    Raises:
        RuntimeError: If forecasting fails.
    """
    logger.info("Forecasting revenue")

    try:
        return _predictor.predict(metric='revenue',periods=periods)
    except Exception as exc:
        logger.exception(
            "Revenue forecast failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to forecast revenue."
        ) from exc