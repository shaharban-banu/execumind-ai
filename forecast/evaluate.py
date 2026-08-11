"""
Forecast model evaluation.
"""

from pathlib import Path
import json

import joblib
from prophet.diagnostics import (cross_validation,performance_metrics,)
from utils.logger import logger


MODEL_DIR = Path("data/models")
REPORT_DIR = Path("data/forecast_reports")

REPORT_DIR.mkdir(parents=True,exist_ok=True,)

SUPPORTED_METRICS = [
    "revenue",
    "orders",
    "customers",
    "aov",
]

def evaluate_model(metric: str):

    logger.info(
        "Evaluating %s model",
        metric,
    )

    model = joblib.load(
        MODEL_DIR / f"{metric}.pkl"
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
        REPORT_DIR / f"{metric}_metrics.json",
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

def evaluate_all():

    reports = {}

    for metric in SUPPORTED_METRICS:

        reports[metric] = evaluate_model(
            metric
        )

    return reports

if __name__ == "__main__":

    reports = evaluate_all()

    for metric, values in reports.items():

        print(metric)

        print(values)