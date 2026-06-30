"""
LangGraph Nodes.

Each node wraps a specialist agent and updates
the shared graph state.
"""

from graph.state import ExecuMindState

from agents.customer_agent import CustomerAgent
from agents.data_agent import DataAgent
from agents.forecast_agent import ForecastAgent

from utils.logger import logger
# --------------------------------------------------
# Agent instances
# --------------------------------------------------

customer_agent = CustomerAgent()

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

    state["customer_analysis"] = response.result

    return state


# --------------------------------------------------
# Data Node
# --------------------------------------------------

def data_node(state: ExecuMindState,) -> ExecuMindState:
    """
    Execute the Data Intelligence Agent.
    """

    logger.info("Running Data Agent")

    response = data_agent.run(state["question"])

    state["data_analysis"] = response.result

    return state


# --------------------------------------------------
# Forecast Node
# --------------------------------------------------

def forecast_node(state: ExecuMindState,) -> ExecuMindState:
    """
    Execute the Forecast Intelligence Agent.
    """

    logger.info("Running Forecast Agent")

    response = forecast_agent.run(state["question"])

    state["forecast_analysis"] = response.result

    return state