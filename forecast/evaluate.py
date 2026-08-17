"""
Forecast model evaluation.
"""

from pathlib import Path
import json

import joblib
from prophet.diagnostics import (cross_validation,performance_metrics,)
from utils.logger import logger

SUPPORTED_METRICS = [
    "revenue",
    "orders",
    "customers",
    "aov",
]
def _get_model_dir(user_id: int) -> Path:
    model_dir = Path(f"data/users/{user_id}/models")
    model_dir.mkdir(parents=True, exist_ok=True)
    return model_dir


def _get_report_dir(user_id: int) -> Path:
    report_dir = Path(f"data/users/{user_id}/forecast_reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir

def evaluate_model(user_id:int,metric: str):

    logger.info(
        "Evaluating %s model",
        metric,
    )

    model = joblib.load(
        _get_model_dir(user_id) / f"{metric}.pkl"
    )

    df_cv = cross_validation(
        model,
        initial="540 days",
        period="30 days",
        horizon="30 days"
    )

    df_perf = performance_metrics(df_cv)
    
    report = {
    "MAE": df_perf["mae"].mean(),
    "RMSE": df_perf["rmse"].mean(),
    "MAPE": df_perf["mape"].mean() * 100,
}

    with open(
        _get_report_dir(user_id) / f"{metric}_metrics.json",
        "w",
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
        )

    logger.info(
        "%s evaluation complete",
        metric,
    )

    return report

def evaluate_all(user_id:int):

    reports = {}

    for metric in SUPPORTED_METRICS:

        reports[metric] = evaluate_model(
            user_id,metric
        )

    return reports

if __name__ == "__main__":

    reports = evaluate_all()

    for metric, values in reports.items():

        print(metric)

        print(values)