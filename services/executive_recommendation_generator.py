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


class ExecutiveRecommendationGenerator:
    """
    Generates executive recommendations from the
    current canonical dataset.
    """

    def __init__(self):
        self.recommendation_service = ExecutiveRecommendationService()

    def generate(self):
        """
        Generate executive recommendations
        from the current dataset.
        """

        # Customer Analysis
        customer_response = get_customer_agent().run(
            CUSTOMER_EXECUTIVE_QUESTION
        )

        # Data Analysis
        data_response = data_agent.run(
            DATA_EXECUTIVE_QUESTION,mode="executive",
        )

        # Forecast Analysis
        forecast_response = forecast_agent.run(
            FORECAST_EXECUTIVE_QUESTION
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

        executive_analysis = executive_agent.run(
            EXECUTIVE_SYNTHESIS_QUESTION,
            context=context,
        )

        self.recommendation_service.delete_all()
        self.recommendation_service.save_recommendations(executive_analysis.result)

        return executive_analysis

