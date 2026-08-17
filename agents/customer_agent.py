"""
Customer Intelligence Agent.
"""

from utils.logger import logger

from agents.base_agent import BaseAgent
from rag.AdavancedRAGpipeline import AdvancedRAGPipeline
from schemas.customer import CustomerAnalysis
from services.context_formatter import format_context


class CustomerIntelligenceAgent(BaseAgent):
    """
    Customer Intelligence Agent.

    Uses the Unified Hybrid RAG pipeline to answer
    customer intelligence questions.
    """

    PROMPT_FILE = "customer_agent.txt"

    RESPONSE_SCHEMA = CustomerAnalysis

    def __init__(
        self,
        rag_pipeline: AdvancedRAGPipeline,
        llm_service=None,
    ):
        super().__init__(llm_service)

        self.rag_pipeline = rag_pipeline

        logger.info("Customer Intelligence Agent initialized successfully.")

    def _retrieve_context(
        self,
        question: str,user_id:int
    ):
        """
        Retrieve supporting documents using
        the Unified Hybrid RAG Pipeline.
        """

        logger.info(
            "Retrieving customer context..."
        )

        try:
            context = self.rag_pipeline.retrieve(query=question,user_id=user_id)

            logger.info(
                "Retrieved %d documents from RAG pipeline.",
                len(context),
            )

            return context
        except Exception as exc:
            logger.exception(
                "Failed to retrieve customer context: %s",
                exc,
            )
            raise RuntimeError(
                "Unable to retrieve customer context."
            ) from exc

    def _prepare_prompt(
        self,
        question: str,
        context,
    ):
        """
        Build final prompt.
        """
        try:
            reviews = []
            business_docs = []

            for doc in context:

                if doc.metadata.get("source") == "reviews":
                    reviews.append(doc)

                elif doc.metadata.get("source") == "business_document":
                    business_docs.append(doc)
            # reviews = reviews[:5]
            # business_docs = business_docs[:5]

            prompt = self.load_prompt()

            formatted_context = format_context(
                reviews=reviews,
                business_docs=business_docs,
            )

            logger.debug(
                    "Prompt prepared with %d reviews and %d business documents.",
                    len(reviews),
                    len(business_docs),
                )

            return prompt.format(
                question=question,
                context=formatted_context,
            )

        except Exception as exc:
            logger.exception(
                "Failed to prepare customer prompt: %s",
                exc,
            )
            raise RuntimeError(
                "Customer prompt preparation failed."
            ) from exc