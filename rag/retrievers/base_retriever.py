"""
Abstract base class for retrievers.
"""

from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseRetriever(ABC):
    """
    Base class for all retrievers.
    """

    @abstractmethod
    def retrieve(self,query: str,top_k: int = 5,) -> list[Document]:
        """
        Retrieve relevant documents.

        Args:
            query: User query.
            top_k: Number of documents.

        Returns:
            Retrieved documents.
        """
        raise NotImplementedError