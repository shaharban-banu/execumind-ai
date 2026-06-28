"""
Data Intelligence Schema.
"""

from pydantic import BaseModel
from schemas.common import (KPI,Recommendation,)

class DataAnalysis(BaseModel):
    executive_summary:str
    kpis:list[KPI]
    trends:list[str]
    anomalies:list[str]
    recommendation:list[Recommendation]
