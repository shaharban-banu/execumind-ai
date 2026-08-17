"""
Compare Prophet vs Naive baseline.
"""

from pathlib import Path
import json

METRICS = [
    "revenue",
    "orders",
    "customers",
    "aov",
]

def get_report_dir(user_id: int) -> Path:
    return Path(f"data/users/{user_id}/forecast_reports")


def compare_models(user_id: int):

    report_dir = get_report_dir(user_id)

    print("=" * 70)
    print("Forecast Model Comparison")
    print("=" * 70)

    for metric in METRICS:

        with open(report_dir / f"{metric}_metrics.json") as f:
            prophet = json.load(f)

        with open(report_dir / f"{metric}_baseline.json") as f:
            baseline = json.load(f)

        print(f"\n{metric.upper()}")
        print("-" * 40)
        print(f"Baseline MAPE : {baseline['MAPE']:.2f}%")
        print(f"Prophet  MAPE : {prophet['MAPE']:.2f}%")

        if prophet["MAPE"] < baseline["MAPE"]:
            print("✓ Prophet performs better")
        else:
            print("✓ Baseline performs better")

if __name__ == "__main__":
    compare_models(user_id=1)