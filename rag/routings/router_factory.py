"""
Factory for creating retrieval routers.
"""

from __future__ import annotations

from rag.config.rag_config import RAGConfig
from rag.routings.base_router import BaseRouter
from rag.routings.rule_based_router import RuleBasedRouter
from rag.routings.llm_router import LLMRouter


class RouterFactory:
    """
    Factory for creating retrieval routers.
    """

    _ROUTERS = {
        "rule": RuleBasedRouter,
        "llm": LLMRouter,
    }

    @classmethod
    def create_router(cls,config: RAGConfig,llm=None,) :
        """
        Create a retrieval router.

        Args:
            config: RAG configuration.
            llm: Language model.

        Returns:
            Retrieval router.
        """

        router_class = cls._ROUTERS.get(
            config.router_type
        )

        if router_class is None:
            raise ValueError(
                f"Unsupported router type: {config.router_type}"
            )

        if config.router_type == "llm":

            if llm is None:
                raise ValueError(
                    "LLMRouter requires an LLM instance."
                )

            return router_class(
                llm=llm,
                config=config,
            )

        return router_class(config=config)