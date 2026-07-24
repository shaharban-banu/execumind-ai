"""
Data Intelligence Schema.
"""

from pydantic import BaseModel,Field
from schemas.common import (KPI,Recommendation,)

class Trend(BaseModel):
    trend: str
    direction: str

class Anomaly(BaseModel):
    anomaly: str
    description: str

class DataAnalysis(BaseModel):
    executive_summary:str
    kpis:list[KPI]
    trends:list[Trend] = Field(default_factory=list)
    anomalies:list[Anomaly] = Field(default_factory=list)
    recommendations:list[Recommendation] = Field(default_factory=list)
