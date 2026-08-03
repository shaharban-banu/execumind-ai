"""
ExecuMind LangGraph Workflow.

Defines the multi-agent workflow for
Customer, Data, and Forecast agents.
"""

from langgraph.graph import (StateGraph,START,END,)

from graph.state import ExecuMindState
from graph.nodes import (planner_node,executive_node)
from utils.logger import logger

def planner_router(state: ExecuMindState) -> str:
    """
    Route execution after the planner.

    Returns:
        "end" if the question is out of context.
        "executive" otherwise.
    """
    logger.info("Router state: %s", state)
    if state.get("status") == "out_of_context":
        return "end"

    return "executive"

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
        "planner_agent",
        planner_node,
    )
    

    workflow.add_node(
        "executive_agent",
        executive_node,
    )
    # ---------------------------------------
    # Define workflow
    # ---------------------------------------
    workflow.add_edge(
        START,
        "planner_agent",
    )

    workflow.add_conditional_edges(
    "planner_agent",
    planner_router,
    {
        "executive": "executive_agent",
        "end": END,
    },
)

    workflow.add_edge(
        "executive_agent",
        END,
    )
   

    return workflow.compile()


graph = build_graph()

if __name__ == "__main__":
    state = {
         "question": "Produce a CEO-level business performance report."
    }

    result = graph.invoke(state)

    print(result)