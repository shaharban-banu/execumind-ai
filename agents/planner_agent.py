"""
Planner Agent.
"""

from agents.base_agent import BaseAgent
from schemas.planner import PlannerDecision


class PlannerAgent(BaseAgent):
    """
    Decides which specialist agents
    should answer the user's question.
    """

    PROMPT_FILE = "planner_agent.txt"

    RESPONSE_SCHEMA = PlannerDecision

    def _retrieve_context(self, question: str, **kwargs):
        return {}

    def _prepare_prompt(self, question: str, context):
        prompt = self.load_prompt()

        return prompt.format(
            question=question,
        )