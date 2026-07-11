"""
Planner schema.
"""

from typing import List
from pydantic import BaseModel, Field


class PlannerDecision(BaseModel):
    """
    Planner output.
    """

    selected_agents: List[str] = Field(
        description=(
            "Agents required to answer the question. "
            "Valid values: customer, data, forecast."
        )
    )

    reasoning: str = Field(
        description="Reason for selecting the agents."
    )