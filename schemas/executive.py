"""
Executive Advisor Schema.
"""

from pydantic import BaseModel
from schemas.common import (Recommendation,)


class ExecutiveAnalysis(BaseModel):

    executive_summary: str

    customer_insights: list[str]

    business_insights: list[str]

    forecast_insights: list[str]

    strategic_recommendations: list[Recommendation]

    confidence: float