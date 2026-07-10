"""
Abstract base class for document preprocessors.
"""

from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BasePreprocessor(ABC):
    """
    Base class for all document preprocessors.
    """

    @abstractmethod
    def process(self,documents: list[Document],) :
        """
        Process a collection of documents.
        """
        raise NotImplementedError