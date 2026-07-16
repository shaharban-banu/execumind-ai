"""
Abstract base class for all document loaders.

Every loader converts a data source into a list of LangChain
Document objects for downstream RAG processing.
"""
from abc import ABC,abstractmethod


class BaseLoader(ABC):
    @abstractmethod
    def load(self):
        """load document from the source
        Returns:
            List[Document]: Loaded documents."""
        raise NotImplementedError