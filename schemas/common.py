"""
Common response schemas.

Shared business objects used by
multiple ExecuMind AI agents.
"""
from pydantic import BaseModel,Field

class Evidence(BaseModel):
    """
    Supporting evidence retrieved
    from reviews or business documents.
    """

    source:str=Field(description="Knowledge source")
    reference:str=Field(description="Review ID or document page.")
    text:str=Field(description="Evidence text")
class Issue(BaseModel):
    """
    Business issue identified by an agent.
    """
    title:str=Field(description="Issue title")
    description:str=Field(description="Issue description")
    severity:str=Field(description="Low|Medium|High")

class Recommendation(BaseModel):
    """
    Executive recommendation.
    """
    priority:str=Field(description="High|Medium|low")
    action: str = Field(description="Recommended action.")
    rationale: str = Field(description="Why this recommendation is made.")

class KPI(BaseModel):
    """
    Business KPI.
    """

    metric: str = Field(description="Metric name.")
    value: float = Field(description="Metric value.")
    unit: str = Field(description="Metric unit.")


class Prediction(BaseModel):
    """
    Forecast prediction.
    """
    metric: str = Field(description="Forecast metric.")
    predicted_value: float = Field(description="Predicted value.")
    confidence: float = Field(description="Prediction confidence.")