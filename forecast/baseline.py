"""
Naive baseline forecasting.

Forecast(t) = Actual(t-1)
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

from forecast.forecasting import load_time_series


REPORT_DIR = Path("forecast/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


SUPPORTED_METRICS = [
    "revenue",
    "orders",
    "customers",
    "aov",
]


def evaluate_baseline(metric: str):

    df = load_time_series(metric).copy()

    # previous month's value
    df["prediction"] = df["y"].shift(1)

    df = df.dropna()
    df_nonzero = df[df["y"] != 0]

    mae = mean_absolute_error(
        df["y"],
        df["prediction"],
    )

    rmse = np.sqrt(mean_squared_error(
        df["y"],
        df["prediction"],
    ))

    mape = (
    (
        (df_nonzero["y"] - df_nonzero["prediction"]).abs()
        / df_nonzero["y"]
    ).mean()
    ) * 100

    report = {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2),
    }

    with open(
        REPORT_DIR / f"{metric}_baseline.json",
        "w",
    ) as f:
        json.dump(report, f, indent=4)

    return report


def evaluate_all():

    reports = {}

    for metric in SUPPORTED_METRICS:

        reports[metric] = evaluate_baseline(metric)

    return reports


if __name__ == "__main__":

    reports = evaluate_all()

    for metric, values in reports.items():

        print(metric)

        print(values)