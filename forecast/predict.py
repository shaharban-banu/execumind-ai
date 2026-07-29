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


class ForecastPredictor:
    """
    Forecast prediction service.

    Loads trained Prophet models, generates future forecasts, retrieves
    validation metrics, and produces executive forecasting insights.
    """
    MODEL_DIR=Path("forecast/models")
    REPORT_DIR = Path("forecast/reports")

    def __init__(self):
        """
        Initialize the Forecast Predictor.

        Creates an in-memory cache for loaded Prophet models to avoid
        repeatedly loading the same model from disk during forecast
        generation.
        """
        self.models={}

    def _load_model(self,metric):
        """
        Load a trained Prophet model.

        Args:
            metric: Forecast metric.

        Returns:
            Loaded Prophet model.

        Raises:
            FileNotFoundError: If the trained model does not exist.
            RuntimeError: If the model cannot be loaded.
        """
        
        if metric in self.models:
            return self.models[metric]
        
        model_path=self.MODEL_DIR/f"{metric}.pkl"

        if not model_path.exists():
            raise FileNotFoundError(
                "Forecast models not found. "
                "Process the platform before requesting forecasts."
            )
        logger.info("Loading %s forecast model ",metric)

        try:
            model=joblib.load(model_path)
        except Exception as exc:
            logger.exception(
                "Failed to load '%s' model: %s",
                metric,
                exc,
            )
            raise RuntimeError(
                f"Unable to load forecast model '{metric}'."
            ) from exc 
        
        self.models[metric]=model
        return model
    

    def _load_metrics(self, metric: str):
        """
        Load evaluation metrics for a forecast model.

        Reads the evaluation metrics stored for the specified forecast
        metric from the reports directory.

        Args:
            metric: Forecast metric (for example, ``revenue`` or
                ``orders``).

        Returns:
            Dictionary containing evaluation metrics if available;
            otherwise ``None``.

        Raises:
            RuntimeError: If the metrics file cannot be read.
        """
        metrics_path = self.REPORT_DIR / f"{metric}_metrics.json"

        if not metrics_path.exists():
            return None

        with open(metrics_path, "r") as f:
            return json.load(f)
    def _load_validation_metrics(self, metric: str):
        """
        Load forecast validation metrics.

        Retrieves the rolling cross-validation results for the specified
        forecast metric and formats them for inclusion in forecast
        responses.

        Args:
            metric: Forecast metric.

        Returns:
            Dictionary containing the validation status, evaluation
            method, and performance metrics. Returns a status of
            ``"Not Evaluated"`` if no validation report exists.

        Raises:
            RuntimeError: If the validation report cannot be loaded or
            parsed.
        """
        report_path = self.REPORT_DIR / f"{metric}_metrics.json"

        if not report_path.exists():
            return {
                "status": "Not Evaluated"
            }
        try:
            with open(report_path, "r") as f:
                metrics = json.load(f)
        except Exception as exc:
            logger.exception(
                "Failed to load validation metrics for '%s': %s",
                metric,
                exc,
            )
            raise RuntimeError(
                "Unable to load validation metrics."
            ) from exc

        logger.debug("Loaded validation metrics for '%s': %s",metric,metrics,)

        return {
            "status": "Evaluated",
            "method": "Rolling Cross Validation",
            "metrics": {
                "MAE": round(metrics["MAE"], 2),
                "RMSE": round(metrics["RMSE"], 2),
                "MAPE": round(metrics["MAPE"], 2),
            },
        }   

    def generate_forecast_insights(self,confidence: dict,validation: dict,):
        """
        Generate executive forecast insights.

        Produces high-level business insights based on forecast confidence
        and validation metrics, including the expected trend, forecast
        risk, and strategic recommendation.

        Args:
            confidence: Forecast confidence information.
            validation: Forecast validation metrics.

        Returns:
            Dictionary containing the forecast trend, risk assessment,
            and business recommendation.
        """
        metrics = validation.get("metrics")

        if metrics is None:
            mape = None
        else:
            mape = metrics["MAPE"]

        confidence_level = confidence["level"]

        # Trend
        trend = (
            "Revenue is expected to remain stable over the forecast horizon."
        )

        # Risk
        if mape is None:
            risk = (
                "Forecast validation metrics are not available."
            )
        elif mape > 20:
            risk = (
                "Forecast uncertainty is relatively high. Business conditions may affect prediction accuracy."
            )
        else:
            risk = (
                "Forecast uncertainty is low, but changes in customer demand should be monitored."
            )

        # Recommendation
        if confidence_level.lower() == "high":
            recommendation = (
                "Use this forecast to support inventory and operational planning."
            )
        else:
            recommendation = (
                "Review forecast regularly and combine it with current business performance before making strategic decisions."
            )

        return {
            "trend": trend,
            "risk": risk,
            "recommendation": recommendation,
        }

    def predict(self,metric:str,periods:int=6,frequency:str="MS"):
        """
        Generate future forecasts for a business metric.

        Loads the trained Prophet model, generates historical and future
        predictions, retrieves confidence and validation information, and
        produces executive forecast insights.

        Args:
            metric: Forecast metric to predict.
            periods: Number of future periods to forecast.
            frequency: Frequency of the forecast periods (default is
                monthly start, ``"MS"``).

        Returns:
            Dictionary containing historical observations, forecasted
            values, confidence information, validation metrics, and
            executive insights.

        Raises:
            FileNotFoundError: If the trained forecast model does not
                exist.
            RuntimeError: If forecast generation fails.
        """
        logger.info("Generating %d-month forecast for '%s'.",periods,metric,)

        try:
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
            insights=self.generate_forecast_insights(confidence,validation)

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
                "insights":insights
            }
        except Exception as exc:
            logger.exception(
                "Forecast generation failed for '%s': %s",
                metric,
                exc,
            )
            raise RuntimeError(
                "Forecast generation failed."
            ) from exc

if __name__=="__main__":
    predictor=ForecastPredictor()
    forecasts=predictor.predict(metric="revenue",periods=6)
    for row in forecasts:
        print(row)
