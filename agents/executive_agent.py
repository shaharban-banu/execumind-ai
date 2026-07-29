"""
Executive Intelligence Agent.

Combines outputs from specialist agents into a
single executive-level business report.
"""

from agents.base_agent import BaseAgent
from schemas.executive import ExecutiveAnalysis
import json
from utils.logger import logger

class ExecutiveAgent(BaseAgent):
    """
    Executive Intelligence Agent.
    """

    PROMPT_FILE = "executive_agent.txt"

    RESPONSE_SCHEMA = ExecutiveAnalysis

    def _retrieve_context(self, question:str,**kwargs):
        """
        Executive Agent does not execute tools.

        It simply receives outputs produced by
        specialist agents.
        """
        logger.debug(
            "Executive Agent does not perform context retrieval."
        )
        return {}
    
    def _prepare_prompt(self, question, context):
        """
        Build executive synthesis prompt.
        """
        try:

            prompt_template = self.load_prompt()

            customer_analysis = context.get("customer_analysis",{})


            data_analysis = context.get("data_analysis",{})

            forecast_analysis =  context.get("forecast_analysis",{})

            logger.info(
                    "Preparing executive prompt with customer, data, "
                    "and forecast analyses."
                )

            return prompt_template.format(
                question=question,
                customer_analysis=json.dumps(customer_analysis, indent=2),
                data_analysis=json.dumps(data_analysis, indent=2),
                forecast_analysis=json.dumps(forecast_analysis, indent=2),
            )

        except Exception as exc:
            logger.exception(
                "Failed to prepare executive prompt: %s",
                exc,
            )
            raise RuntimeError(
                "Executive prompt preparation failed."
            ) from exc

