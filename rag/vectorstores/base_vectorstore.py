"""
Abstract base class for vector stores.
"""

from abc import ABC, abstractmethod
from langchain_core.documents import Document


class BaseVectorStore(ABC):
    """
    Base class for vector stores.
    """

    @abstractmethod
    def build(self,documents: list[Document],embeddings: list[list[float]],) :
        """
        Build vector index.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self):
        """
        Save vector store.
        """
        raise NotImplementedError

    @abstractmethod
    def load(self):
        """
        Load vector store.
        """
        raise NotImplementedError
    
    @abstractmethod
    def search(self,query_embedding: list[float],top_k: int = 5,) -> list[Document]:
        """
        Search the vector store and return the most similar documents.
        """
        raise NotImplementedError