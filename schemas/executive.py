"""
Executive Advisor Schema.
"""

from pydantic import BaseModel,Field
from typing import List
from schemas.common import (Recommendation,Evidence)


class ExecutiveAnalysis(BaseModel):

    executive_summary: str=Field(description="overall executive summary")

    key_findings: List[str] = Field(default_factory=list,description="Most important findings.")

    business_risks: list[str]  = Field(default_factory=list,description="Major business risks.")

    strategic_recommendations: list[Recommendation]= Field(default_factory=list)

    evidence: List[Evidence] = Field(default_factory=list)