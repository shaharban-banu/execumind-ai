"""
Shared LangGraph State.

Defines the shared state exchanged between
all specialist agents.
"""

from typing import TypedDict

from schemas.customer import CustomerAnalysis
from schemas.data import DataAnalysis
from schemas.forecast import ForecastAnalysis

class ExecuMindState(TypedDict, total=False):
    """
    Shared state used by LangGraph.

    Every node reads from and writes to this state.
    """

    # User question
    question: str

    # Agent outputs
    customer_analysis: CustomerAnalysis

    data_analysis: DataAnalysis

    forecast_analysis: ForecastAnalysis

    # Combined evidence (optional)
    evidence: dict