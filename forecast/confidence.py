from pathlib import Path
import json

def _get_report_dir(user_id: int) -> Path:
    report_dir = Path(f"data/users/{user_id}/forecast_reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir

class ForecastConfidence:

    @staticmethod
    def get(user_id:int,metric: str):

        with open(
            _get_report_dir(user_id) / f"{metric}_metrics.json",
            "r",
        ) as f:
            report = json.load(f)

        mape = report["MAPE"]

        if mape < 10:
            level = "Very High"
            score = 95

        elif mape < 20:
            level = "High"
            score = 85

        elif mape < 30:
            level = "Moderate"
            score = 70

        elif mape < 50:
            level = "Low"
            score = 50

        else:
            level = "Very Low"
            score = 30

        return {
            "score": score,
            "level": level,
            "mape": round(mape, 2),
            "baseline_mape": None,
            "summary": f"Forecast reliability is {level.lower()} based on historical model performance.",
            "evaluation_method": "Rolling Cross Validation",
        }