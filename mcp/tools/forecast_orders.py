"""
Order Forecast MCP Tool.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_orders(periods:int=6):
    logger.info("Forecasting orders")
    return _predictor.predict(metric='orders',periods=periods)