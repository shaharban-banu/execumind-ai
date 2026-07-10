"""
Abstract base class for embedding models.
"""

from abc import ABC, abstractmethod


class BaseEmbedder(ABC):
    """
    Base class for embedding models.
    """

    @abstractmethod
    def embed(self,texts: list[str],):
        """
        Generate embeddings.

        Args:
            texts: Input texts.

        Returns:
            Embedding vectors.
        """
        raise NotImplementedError