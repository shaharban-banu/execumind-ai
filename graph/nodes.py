"""
LangGraph Nodes.

Each node wraps a specialist agent and updates
the shared graph state.
"""

from graph.state import ExecuMindState

from agents.customer_agent import CustomerIntelligenceAgent
from agents.data_agent import DataAgent
from agents.forecast_agent import ForecastAgent

from utils.logger import logger
# --------------------------------------------------
# Agent instances
# --------------------------------------------------

customer_agent = CustomerIntelligenceAgent()

data_agent = DataAgent()

forecast_agent = ForecastAgent()


# --------------------------------------------------
# Customer Node
# --------------------------------------------------

def customer_node(state: ExecuMindState,) -> ExecuMindState:
    """
    Execute the Customer Intelligence Agent.
    """

    logger.info("Running Customer Agent")

    response = customer_agent.run(state["question"])

    return {
    "customer_analysis": response.result
}


# --------------------------------------------------
# Data Node
# --------------------------------------------------

def data_node(state: ExecuMindState,) -> ExecuMindState:
    """
    Execute the Data Intelligence Agent.
    """

    logger.info("Running Data Agent")

    response = data_agent.run(state["question"])

    return {
    "data_analysis": response.result
}


# --------------------------------------------------
# Forecast Node
# --------------------------------------------------

def forecast_node(state: ExecuMindState,) -> ExecuMindState:
    """
    Execute the Forecast Intelligence Agent.
    """

    logger.info("Running Forecast Agent")

    response = forecast_agent.run(state["question"])

    return {
    "forecast_analysis": response.result
}

# --------------------------------------------------
# Evidence Aggregation Node
# --------------------------------------------------

def aggregate_evidence_node(
    state: ExecuMindState,
) -> ExecuMindState:
    """
    Aggregate outputs from all specialist agents.
    """

    logger.info("Aggregating agent evidence")

    state["evidence"] = {
        "customer": state.get("customer_analysis"),
        "data": state.get("data_analysis"),
        "forecast": state.get("forecast_analysis"),
    }

    return state