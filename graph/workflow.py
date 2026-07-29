"""
ExecuMind LangGraph Workflow.

Defines the multi-agent workflow for
Customer, Data, and Forecast agents.
"""

from langgraph.graph import (StateGraph,START,END,)

from graph.state import ExecuMindState
from graph.nodes import (planner_node,executive_node)

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

    workflow.add_edge(
        "planner_agent",
        "executive_agent",
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