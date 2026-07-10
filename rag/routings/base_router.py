"""
Abstract base class for retrieval routers.
"""

from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseRouter(ABC):
    """
    Base class for retrieval routers.
    """

    @abstractmethod
    def select_strategy(self,query: str,):
        """
        Retrieve documents.

        Args:
            query: User query.
            top_k: Number of documents.

        Returns:
            Retrieved documents.
        """
        raise NotImplementedError