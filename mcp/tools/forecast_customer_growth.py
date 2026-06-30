"""
Customer Growth Forecast MCP Tool.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_customer_growth(periods:int=6):
    logger.info("Forecasting customer growth")
    return _predictor.predict(metric='customers',periods=periods)