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

    def _get_model_dir(self, user_id: int) -> Path:
        model_dir = Path(f"data/users/{user_id}/models")
        model_dir.mkdir(parents=True, exist_ok=True)
        return model_dir

    def _get_report_dir(self, user_id: int) -> Path:
        report_dir = Path(f"data/users/{user_id}/forecast_reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir

    def train_metric(self,user_id:int,metric):
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
            df=load_time_series(user_id,metric)
        
            logger.debug("Loaded %d observations for '%s'.",len(df),metric,)

            model=Prophet(yearly_seasonality=False,
                        weekly_seasonality=False,
                        daily_seasonality=False,
                        n_changepoints=5,
                        changepoint_prior_scale=0.05,)
            model.fit(df)
            model_path = self._get_model_dir(user_id) / f"{metric}.pkl"
            joblib.dump(model, model_path)

            logger.info("%s model saved to %s", metric, model_path)

            logger.info("Evaluating %s model...", metric)

            evaluate_model(user_id,metric)

        except Exception as exc:
            logger.exception(
                "Failed to train '%s' model: %s",
                metric,
                exc,
            )
            raise RuntimeError(
                f"Model training failed for '{metric}'."
            ) from exc

    def train(self,user_id:int):
        """
        Train all forecasting models.

        Returns:
            Dictionary containing training status.
        """
        self._get_model_dir(user_id)
        self._get_report_dir(user_id)

        self.clear_models(user_id)
        self.clear_reports(user_id)

        logger.info("Starting forecast model training")

        for metric in self.METRICS:
            self.train_metric(user_id,metric)

        return {
            "success": True,
            "models": len(self.METRICS),
            "metrics":self.METRICS,
            "message": "Forecast models trained successfully."
        }
    def clear_models(self,user_id:int):
        """
        Delete all previously trained forecast models.
        """

        model_dir = self._get_model_dir(user_id)

        for model_file in model_dir.glob("*.pkl"):
            logger.info("Removing old model: %s", model_file.name)
            model_file.unlink()

    def clear_reports(self,user_id:int):
        """
        Delete previously generated forecast evaluation reports.
        """

        report_dir = self._get_report_dir(user_id)

        for report_file in report_dir.glob("*_metrics.json"):
            logger.info("Removing old report: %s", report_file.name)
            report_file.unlink()