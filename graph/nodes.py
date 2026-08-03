"""
LangGraph Nodes.

Each node wraps a specialist agent and updates
the shared graph state.
"""

from graph.state import ExecuMindState

from agents.customer_agent import CustomerIntelligenceAgent
from agents.data_agent import DataAgent
from agents.forecast_agent import ForecastAgent
from agents.executive_agent import ExecutiveAgent
from agents.planner_agent import PlannerAgent
from rag.services.pipeline_service import create_pipeline

from utils.logger import logger

logger.info("Loading RAG pipeline...")


# --------------------------------------------------
# Agent instances
# --------------------------------------------------

data_agent = DataAgent()

forecast_agent = ForecastAgent()

executive_agent = ExecutiveAgent()

planner_agent = PlannerAgent()

def get_customer_agent():
    """
    Create a Customer Intelligence Agent.

    Initializes the Advanced RAG pipeline and returns a configured
    Customer Intelligence Agent instance.

    Returns:
        Configured CustomerIntelligenceAgent instance.

    Raises:
        RuntimeError: If the RAG pipeline cannot be created.
    """
    rag_pipeline = create_pipeline()
    return CustomerIntelligenceAgent(rag_pipeline)

# --------------------------------------------------
# Planner Node
# --------------------------------------------------
def planner_node(state: ExecuMindState):
    """
    Execute the Planner Agent.

    Determines which specialist agents should be invoked to answer the
    user's question and stores the planning decision in the shared graph
    state.

    Args:
        state: Current LangGraph execution state.

    Returns:
        Dictionary containing the planner decision.

    Raises:
        RuntimeError: If planner execution fails.
    """
    try:

        logger.info("Running Planner Agent")

        response = planner_agent.run(
            state["question"],history=state.get("history", []),
        )
        logger.info(
    "Planner Decision: %s",
    response.result.model_dump()
)
        if len(response.result.selected_agents)==0:
            return {
                "planner_decision": response.result,
                "status": "out_of_context",
                "message": (
                    "I'm designed to answer questions about your uploaded "
                    "business data and knowledge base. "
                    "Please ask about sales, customers, forecasts, "
                    "products, revenue, or executive strategy."
                )
            }

        logger.info("Planner selected: %s",response.result.selected_agents,)
        logger.info("Planner reasoning: %s",response.result.reasoning,)

        return {
            "planner_decision": response.result
        }
    except Exception as exc:
        logger.exception(
            "Planner node execution failed: %s",
            exc,
        )
        raise RuntimeError(
            "Planner node failed."
        ) from exc
# --------------------------------------------------
# Executive Node
# --------------------------------------------------

def executive_node(state: ExecuMindState,) -> ExecuMindState:
    """
    Execute the selected specialist agents.

    Runs the specialist agents chosen by the Planner Agent, collects their
    outputs, and passes the combined context to the Executive Agent to
    produce the final executive business report.

    Args:
        state: Current LangGraph execution state.

    Returns:
        Updated graph state containing specialist analyses and the final
        executive analysis.

    Raises:
        RuntimeError: If a required knowledge base is unavailable or any
            agent execution fails.

    """
    try:
        logger.info("Running Executive Agent")

        decision=state["planner_decision"]

        context = {}

        if "customer" in decision.selected_agents:
            
            if not get_customer_agent().rag_pipeline.is_ready():
                raise RuntimeError(
                    "Knowledge base is not ready. Please process the platform first."
                )
            logger.info("Executing Customer Agent")

            response = get_customer_agent().run(
                state["question"]
            )

            customer = response.result

            context["customer_analysis"] = customer.model_dump(exclude={"evidence"})

        if "data" in decision.selected_agents:

            logger.info("Executing Data Agent")

            response = data_agent.run(
                state["question"]
            )

            data = response.result
            context["data_analysis"] = data.model_dump(exclude={"evidence"})

        if "forecast" in decision.selected_agents:

            logger.info("Executing Forecast Agent")

            response = forecast_agent.run(
                state["question"]
            )

            forecast = response.result
            context["forecast_analysis"] =forecast.model_dump(exclude={"evidence"})

        logger.info("Generating Executive Report")

        executive_response = executive_agent.run(
            question=state["question"],
            context=context,
        )

        return {
            **context,
            "executive_analysis": executive_response.result,
        }

    except Exception as exc:
        logger.exception(
            "Executive node execution failed: %s",
            exc,
        )
        raise RuntimeError(
            "Executive node failed."
        ) from exc