"""
ExecuMind LangGraph Workflow.

Defines the multi-agent workflow for
Customer, Data, and Forecast agents.
"""

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from graph.state import ExecuMindState
from graph.nodes import (customer_node,data_node,forecast_node,)

def build_graph():
    """
    Build the ExecuMind LangGraph workflow.

    Returns:
        Compiled LangGraph workflow.
    """

    workflow = StateGraph(ExecuMindState)

    # ---------------------------------------
    # Register nodes
    # ---------------------------------------

    workflow.add_node(
        "customer_agent",
        customer_node,
    )

    workflow.add_node(
        "data_agent",
        data_node,
    )

    workflow.add_node(
        "forecast_agent",
        forecast_node,
    )

    # ---------------------------------------
    # Define workflow
    # ---------------------------------------

    workflow.add_edge(
        START,
        "customer_agent",
    )

    workflow.add_edge(
        "customer_agent",
        "data_agent",
    )

    workflow.add_edge(
        "data_agent",
        "forecast_agent",
    )

    workflow.add_edge(
        "forecast_agent",
        END,
    )

    return workflow.compile()


graph = build_graph()