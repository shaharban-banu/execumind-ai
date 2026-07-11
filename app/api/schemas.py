"""
API request/response schemas.
"""

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class HealthResponse(BaseModel):
    status: str