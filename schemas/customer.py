"""
Customer Intelligence Schema.
"""
from pydantic import BaseModel,Field
from schemas.common import (Evidence,Recommendation)

class Issue(BaseModel):
    title: str
    description: str
    severity: str


class CustomerAnalysis(BaseModel):
    executive_summary: str

    issues: list[Issue] = Field(default_factory=list)

    recommendations: list[Recommendation] = Field(default_factory=list)

    evidence: list[Evidence] = Field(default_factory=list)
# class CustomerAnalysis(BaseModel):
#     executive_summary:str
#     key_findings:list[Issue]
#     evidence:list[Evidence]
#     risks:str
#     recommendations:list[Recommendation]