"""
Customer Intelligence Schema.
"""
from pydantic import BaseModel,Field
from schemas.common import (Evidence,Issue,Recommendation)

class CustomerAnalysis(BaseModel):
    executive_summary:str
    issues:list[Issue]
    evidence:list[Evidence]
    business_interpretation:str
    recommendation:list[Recommendation]