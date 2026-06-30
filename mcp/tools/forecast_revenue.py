"""
Revenue Forecast MCP Tool.

Provides revenue forecasting capability
for the Forecast Intelligence Agent.
"""
from forecast.predict import ForecastPredictor
from utils.logger import logger

_predictor=ForecastPredictor()

def forecast_revenue(periods:int=6):
    logger.info("Forecasting revenue")
    return _predictor.predict(metric='revenue',periods=periods)