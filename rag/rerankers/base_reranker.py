"""
Abstract base class for document rerankers.
"""

from abc import ABC, abstractmethod
from langchain_core.documents import Document


class BaseReranker(ABC):
    """
    Base class for rerankers.
    """

    @abstractmethod
    def rerank(self,query: str,documents: list[Document],top_k: int,) :
        """
        Rerank retrieved documents.

        Args:
            query: User query.
            documents: Retrieved documents.
            top_k: Number of documents to return.

        Returns:
            Reranked documents.
        """
        raise NotImplementedError