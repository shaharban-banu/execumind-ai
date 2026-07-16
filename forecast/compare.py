"""
Compare Prophet vs Naive baseline.
"""

from pathlib import Path
import json


REPORT_DIR = Path("forecast/reports")


METRICS = [
    "revenue",
    "orders",
    "customers",
    "aov",
]


print("=" * 70)
print("Forecast Model Comparison")
print("=" * 70)

for metric in METRICS:

    with open(REPORT_DIR / f"{metric}_metrics.json") as f:
        prophet = json.load(f)

    with open(REPORT_DIR / f"{metric}_baseline.json") as f:
        baseline = json.load(f)

    print(f"\n{metric.upper()}")

    print("-" * 40)

    print(
        f"Baseline MAPE : {baseline['MAPE']:.2f}%"
    )

    print(
        f"Prophet  MAPE : {prophet['MAPE']:.2f}%"
    )

    if prophet["MAPE"] < baseline["MAPE"]:
        print("✓ Prophet performs better")
    else:
        print("✓ Baseline performs better")