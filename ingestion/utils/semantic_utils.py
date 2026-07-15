"""
semantic_utils.py

Utility functions for semantic preprocessing.
"""

from ingestion.mappings.synonyms import SYNONYMS
from ingestion.utils.normalize import TextNormalizer


class SemanticUtils:
    """
    Helper methods for semantic preprocessing.
    """

    @staticmethod
    def normalize_and_replace(text: str) -> str:
        """
        Normalize text and replace known business synonyms.
        """

        normalized = TextNormalizer.normalize(text)

        # ----------------------------------------
        # Remove common dataset prefixes
        # ----------------------------------------

        prefixes = [
            "olist",
            "flipkart",
            "amazon",
            "shopify",
            "ecommerce",
        ]

        words = [
            word
            for word in normalized.split()
            if word not in prefixes
        ]

        # ----------------------------------------
        # Remove common suffixes
        # ----------------------------------------

        suffixes = {
            "dataset",
            "table",
            "data",
            "csv",
            "file",
        }

        words = [
            word
            for word in words
            if word not in suffixes
        ]

        # ----------------------------------------
        # Apply synonym replacement
        # ----------------------------------------

        normalized_words = [
            SYNONYMS.get(word, word)
            for word in words
        ]

        return " ".join(normalized_words)