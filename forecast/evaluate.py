"""
Forecast model evaluation.
"""

from pathlib import Path
import json

import joblib
from prophet.diagnostics import (cross_validation,performance_metrics,)
from utils.logger import logger


MODEL_DIR = Path("forecast/models")
REPORT_DIR = Path("forecast/reports")

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
    # print(f"\n========== {metric.upper()} Cross Validation ==========\n")
    # print(df_cv[["ds", "y", "yhat"]].head(20))

    # print("\n========== Smallest Actual Revenue ==========\n")
    # print(df_cv.nsmallest(10, "y")[["ds", "y", "yhat"]])

    # print(f"\n========== {metric.upper()} Statistics ==========\n")
    # print(df_cv["y"].describe())

    # print("Number of CV rows:", len(df_cv))

    # print(df_cv.head())

    # print(df_cv.tail())

    # print(df_cv["cutoff"].unique())

    # print(df_cv["ds"].min())

    # print(df_cv["ds"].max())

    df_perf = performance_metrics(df_cv)

    
    # print(df_perf.head())
    # print(df_perf.tail())
    # print(df_cv[["y", "yhat"]].head())
    
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