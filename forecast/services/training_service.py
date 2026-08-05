"""
Forecast Training Service.

Trains all supported forecasting models
using the canonical SQLite database.
"""

from utils.logger import logger
import joblib
from pathlib import Path
from prophet import Prophet
from forecast.forecasting import load_time_series
from forecast.evaluate import evaluate_model

class ForecastTrainingService:
    """
    Trains Prophet forecasting models
    from the current canonical dataset.
    """

    METRICS = [
        "revenue",
        "orders",
        "customers",
        "aov",
    ]

    MODEL_DIR = Path("data/models")
    REPORT_DIR = Path("data/forecast_reports")

    def train_metric(self,metric):
        """
        Train and save a Prophet forecasting model.

        Loads historical time-series data for the specified metric,
        trains a Prophet model, and stores the trained model on disk.

        Args:
            metric: Forecast metric to train.

        Raises:
            RuntimeError: If model training or saving fails.
        """
        logger.info("Training Prophet model %s",metric)

        try:
            df=load_time_series(metric)
        
            logger.debug("Loaded %d observations for '%s'.",len(df),metric,)

            model=Prophet(yearly_seasonality=False,
                        weekly_seasonality=False,
                        daily_seasonality=False,
                        n_changepoints=5,
                        changepoint_prior_scale=0.05,)
            model.fit(df)
            model_path = self.MODEL_DIR / f"{metric}.pkl"
            joblib.dump(model, model_path)

            logger.info("%s model saved to %s", metric, model_path)

            logger.info("Evaluating %s model...", metric)

            evaluate_model(metric)

        except Exception as exc:
            logger.exception(
                "Failed to train '%s' model: %s",
                metric,
                exc,
            )
            raise RuntimeError(
                f"Model training failed for '{metric}'."
            ) from exc

    def train(self):
        """
        Train all forecasting models.

        Returns:
            Dictionary containing training status.
        """
        self.MODEL_DIR.mkdir(parents=True, exist_ok=True)

        self.clear_models()
        self.clear_reports()

        logger.info("Starting forecast model training")

        for metric in self.METRICS:
            self.train_metric(metric)

        return {
            "success": True,
            "models": len(self.METRICS),
            "metrics":self.METRICS,
            "message": "Forecast models trained successfully."
        }
    def clear_models(self):
        """
        Delete all previously trained forecast models.
        """

        self.MODEL_DIR.mkdir(parents=True, exist_ok=True)

        for model_file in self.MODEL_DIR.glob("*.pkl"):
            logger.info("Removing old model: %s", model_file.name)
            model_file.unlink()

    def clear_reports(self):
        """
        Delete previously generated forecast evaluation reports.
        """

        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)

        for report_file in self.REPORT_DIR.glob("*_metrics.json"):
            logger.info(
                "Removing old report: %s",
                report_file.name,
            )
            report_file.unlink()