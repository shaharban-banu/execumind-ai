"""
Forecast Schema.
"""

from pydantic import BaseModel,Field
from schemas.common import (Prediction,Recommendation,Evidence,KPI)

class ForecastAnalysis(BaseModel):
    executive_summary:str=Field(description="Executive summary of forecast findings.")
    #predictions:list[Prediction]=Field(description="Forecast predictions.")
    risks:list[str]=Field(description="Potential risks identified.")
    recommendation:list[Recommendation]=Field(description="Recommended executive actions.")
    forecast_period: str = Field(description="Forecast horizon, e.g. 'Next 30 Days'.")
    key_kpis: list[KPI] = Field(description="Forecasted business KPIs.")
    evidence: list[Evidence] = Field(description="Evidence supporting the forecast.")
    business_impact: str = Field(description="Business interpretation of forecast.")