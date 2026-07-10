"""
Abstract base class for document chunkers.
"""

from abc import ABC, abstractmethod
from langchain_core.documents import Document


class BaseChunker(ABC):
    """
    Base class for all chunkers.
    """

    @abstractmethod
    def chunk(self,documents: list[Document],) :
        """
        Split documents into chunks.
        """
        raise NotImplementedError