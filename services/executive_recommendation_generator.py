"""
Executive recommendation generator.

Coordinates customer, data, forecast, and executive
agents to generate executive recommendations.
"""
from utils.logger import logger
from graph.nodes import (
    get_customer_agent,
    data_agent,
    forecast_agent,
    executive_agent,
)

from config.executive_questions import (
    CUSTOMER_EXECUTIVE_QUESTION,
    DATA_EXECUTIVE_QUESTION,
    FORECAST_EXECUTIVE_QUESTION,
    EXECUTIVE_SYNTHESIS_QUESTION,
)

from services.executive_recommendation_service import (
    ExecutiveRecommendationService,
)
from services.platform_status import get_platform_status


class ExecutiveRecommendationGenerator:
    """
    Generates executive recommendations from the
    current canonical dataset.
    """

    def __init__(self):
        """
        Initialize the executive recommendation generator.
        """
        self.recommendation_service = ExecutiveRecommendationService()

    def generate(self,user_id:int):
        """
        Generate executive recommendations
        from the current dataset.
        Runs the customer, data, and forecast agents,
        combines their outputs using the executive agent,
        and persists the generated recommendations.

        Returns:
            Executive agent response.

        Raises:
            RuntimeError:
                If recommendation generation fails.
        """
        logger.info("Starting executive recommendation generation.")
        if not get_platform_status(user_id)["platform_ready"]:
            return {
                "success": False,
                "message": "Platform has not been processed. Please process the platform before generating executive recommendations."
            }

        try:
            # Customer Analysis
            customer_response = get_customer_agent().run(
                CUSTOMER_EXECUTIVE_QUESTION,
                user_id=user_id,
            )

            # Data Analysis
            data_response = data_agent.run(
                DATA_EXECUTIVE_QUESTION,mode="executive",
                user_id=user_id,
            )

            # Forecast Analysis
            forecast_response = forecast_agent.run(
                FORECAST_EXECUTIVE_QUESTION,
                user_id=user_id,
            )

            context = {
                "customer_analysis": customer_response.result.model_dump(
                    exclude={"evidence"}
                ),
                "data_analysis": data_response.result.model_dump(
                    exclude={"evidence"}
                ),
                "forecast_analysis": forecast_response.result.model_dump(
                    exclude={"evidence"}
                ),
            }
            #print(context)
            logger.info("Generating executive synthesis.")

            executive_analysis = executive_agent.run(
                EXECUTIVE_SYNTHESIS_QUESTION,
                context=context,
            )

            self.recommendation_service.delete_all(user_id)
            self.recommendation_service.save_recommendations(user_id,executive_analysis.result)

            logger.info("Executive recommendations generated successfully.")
            return executive_analysis
        except Exception as exc:
            logger.exception(
                "Failed to generate executive recommendations."
            )
            raise RuntimeError(
                "Executive recommendation generation failed."
            ) from exc

