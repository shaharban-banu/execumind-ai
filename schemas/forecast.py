"""
Forecast Schema.
"""

from pydantic import BaseModel
from schemas.common import (Prediction,Recommendation,)

class ForecastAnalysis(BaseModel):
    executive_summary:str
    predictions:list[Prediction]
    risks:list[str]
    recommendation:list[Recommendation]