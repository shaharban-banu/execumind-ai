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

def get_customer_agent():
    rag_pipeline = create_pipeline()
    return CustomerIntelligenceAgent(rag_pipeline)

data_agent = DataAgent()

forecast_agent = ForecastAgent()

executive_agent = ExecutiveAgent()

planner_agent=PlannerAgent()

# --------------------------------------------------
# Planner Node
# --------------------------------------------------
def planner_node(state: ExecuMindState):

    logger.info("Running Planner Agent")

    response = planner_agent.run(
        state["question"]
    )
    logger.info(
        "Planner selected: %s",
        response.result.selected_agents,
    )
    logger.info(
    "Planner reasoning: %s",
    response.result.reasoning,
)

    return {
         "planner_decision": response.result
    }
# --------------------------------------------------
# Executive Node
# --------------------------------------------------

def executive_node(state: ExecuMindState,) -> ExecuMindState:
    """
    Execute selected specialist agents and
    synthesize their outputs.
    """

    logger.info("Running Executive Agent")

    decision=state["planner_decision"]

    context = {}

    if "customer" in decision.selected_agents:
        if not get_customer_agent.rag_pipeline.is_ready():
            raise RuntimeError(
                "Knowledge base is not ready. Please process the platform first."
            )
        logger.info("Executing Customer Agent")

        response = get_customer_agent().run(
            state["question"]
        )

        customer = response.result

        context["customer_analysis"] =customer.model_dump(exclude={"evidence"})

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