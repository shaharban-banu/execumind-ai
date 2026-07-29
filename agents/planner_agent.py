"""
Planner Agent.
"""

from agents.base_agent import BaseAgent
from schemas.planner import PlannerDecision
from utils.logger import logger

class PlannerAgent(BaseAgent):
    """
    Decides which specialist agents
    should answer the user's question.
    """

    PROMPT_FILE = "planner_agent.txt"

    RESPONSE_SCHEMA = PlannerDecision

    def _retrieve_context(self, question: str, **kwargs):
        logger.debug(
            "Planner Agent does not require context retrieval."
        )
        return {}

    def _prepare_prompt(self, question: str, context):

        """
        Prepare the planner prompt.

        Returns:
            Formatted planner prompt.

        """
        try:
            prompt = self.load_prompt()

            logger.info("Planner prompt prepared successfully.")

            return prompt.format(
                question=question,
            )
        except Exception as exc:
            logger.exception(
                "Failed to prepare planner prompt: %s",
                exc,
            )
            raise RuntimeError(
                "Planner prompt preparation failed."
            ) from exc