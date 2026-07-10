"""
Rule-based retrieval strategy router.
"""
from utils.logger import logger
import re
from rag.config.rag_config import RAGConfig
from rag.routings.base_router import BaseRouter

class RuleBasedRouter(BaseRouter):
    """
    Rule-based retrieval strategy router.

    Selects a retrieval strategy using simple heuristics.
    """
    ORDER_PATTERN = re.compile(
        r"\b(order|invoice)\s*[#: -]?\d+\b",
        re.IGNORECASE,
    )

    _REASONING_WORDS = {
        "how",
        "why",
        "improve",
        "increase",
        "decrease",
        "reduce",
        "recommend",
        "strategy",
        "optimize",
        "future",
        "forecast",
    }

    def __init__(self,config:RAGConfig,) :
        """
        Initialize router."""
        self.config = config

    def select_strategy(self,query: str,):
        """
        Select the retrieval strategy.

        Args:
            query: User question.

        Returns:
            Retrieval strategy name.
        """

        if not self.config.router_enabled:
            return self.config.default_retriever

        if (
            self._is_order_lookup(query)
            and "bm25" in self.config.available_retrievers
        ):
            return "bm25"

        if (
            self._is_reasoning_query(query)
            and "hyde" in self.config.available_retrievers
        ):
            return "hyde"

        if "hybrid" in self.config.available_retrievers:
            return "hybrid"

        return self.config.default_retriever

    
    def _is_order_lookup(self,query: str,) :
        """
        Detect order lookup queries.
        """
        return bool(self._ORDER_PATTERN.search(query)        )

    def _is_reasoning_query(self,query: str,) :
        """
        Detect reasoning-oriented questions.
        """

        query = query.lower()

        return any(word in query for word in self._REASONING_WORDS)