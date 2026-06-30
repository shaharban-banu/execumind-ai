"""
Average Order Value Forecast MCP Tool.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_average_order_value(periods:int=6):
    logger.info("Forecasting average  order value")
    return _predictor.predict(metric='aov',periods=periods)