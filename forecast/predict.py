"""
Forecast Prediction Service.

Loads trained Prophet models and generates
future forecasts for supported business metrics.
"""
from pathlib import Path
import joblib 

from utils.logger import logger
from forecast.confidence import ForecastConfidence
import json


MODEL_DIR=Path("forecast/models")
REPORT_DIR = Path("forecast/reports")

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
    

    def _load_metrics(self, metric: str):
        metrics_path = REPORT_DIR / f"{metric}_metrics.json"

        if not metrics_path.exists():
            return None

        with open(metrics_path, "r") as f:
            return json.load(f)
    def _load_validation_metrics(self, metric: str):
        report_path = REPORT_DIR / f"{metric}_metrics.json"

        if not report_path.exists():
            return {
                "status": "Not Evaluated"
            }

        with open(report_path, "r") as f:
            metrics = json.load(f)
        print(metrics)
        return {
            "status": "Evaluated",
            "method": "Rolling Cross Validation",
            "metrics": {
                "MAE": round(metrics["MAE"], 2),
                "RMSE": round(metrics["RMSE"], 2),
                "MAPE": round(metrics["MAPE"], 2),
            },
        }   
    def predict(self,metric:str,periods:int=6,frequency:str="MS"):
        model=self._load_model(metric)

        history = model.history.tail(6)

        history_result = []

        for _, row in history.iterrows():
            history_result.append({
                "date": row["ds"].strftime("%Y-%m"),
                "value": round(row["y"], 2),
            })
            
        future=model.make_future_dataframe(periods=periods,freq=frequency)
        forecast=model.predict(future)
        forecast=forecast.tail(periods)
        result=[]

        confidence = ForecastConfidence.get(metric)
        #metrics = self._load_metrics(metric)
        validation = self._load_validation_metrics(metric)

        for _,row in forecast.iterrows():
            result.append({
                "date":row["ds"].strftime("%Y-%m"),
                "prediction":round(row["yhat"],2),
                "confidence":confidence,
                "lower_bound":round(row["yhat_lower"],2),
                "upper_bound":round(row["yhat_upper"],2),
            })
        logger.info("Generated %d forecasts",len(result))
        return  {
            "history": history_result,
            "forecast": result,
            "confidence": confidence,
            "validation": validation,
        }

if __name__=="__main__":
    predictor=ForecastPredictor()
    forecasts=predictor.predict(metric="revenue",periods=6)
    for row in forecasts:
        print(row)
