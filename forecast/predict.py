"""
Forecast Prediction Service.

Loads trained Prophet models and generates
future forecasts for supported business metrics.
"""
from pathlib import Path
import joblib 
import pandas as pd
from prophet import Prophet
from utils.logger import logger
from forecast.confidence import ForecastConfidence


MODEL_DIR=Path("forecast/models")

class ForecastPredictor:
    def __init__(self):
        self.models={}
    def _load_model(self,metric):
        if metric in self.models:
            return self.models[metric]
        
        model_path=MODEL_DIR/f"{metric}.pkl"
        if not model_path.exists():
            raise FileNotFoundError(f"forecast model not found : {model_path}")
        logger.info("Loading %s forecast model ",metric)

        model=joblib.load(model_path)
        self.models[metric]=model
        return model
    
    def predict(self,metric:str,periods:int=6,frequency:str="MS"):
        model=self._load_model(metric)
        future=model.make_future_dataframe(periods=periods,freq=frequency)
        forecast=model.predict(future)
        forecast=forecast.tail(periods)
        result=[]

        confidence = ForecastConfidence.get(metric)

        for _,row in forecast.iterrows():
            result.append({
                "date":row["ds"].strftime("%Y-%m"),
                "prediction":round(row["yhat"],2),
                "confidence":confidence,
                "lower_bound":round(row["yhat_lower"],2),
                "upper_bound":round(row["yhat_upper"],2),
            })
        logger.info("Generated %d forecasts",len(result))
        return result

if __name__=="__main__":
    predictor=ForecastPredictor()
    forecasts=predictor.predict(metric="revenue",periods=6)
    for row in forecasts:
        print(row)
