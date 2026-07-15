"""
normalizer.py

Utility functions for normalizing table names and column names
before semantic mapping.
"""

import re


class TextNormalizer:
    """
    Utility class for normalizing identifiers.
    """

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize a table or column name.

        Examples
        --------
        CustomerID -> customer id
        CUSTOMER_ID -> customer id
        customer-id -> customer id
        customer.id -> customer id
        Buyer_No -> buyer no
        """

        if not text:
            return ""

        # Split camelCase
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

        # Replace separators with spaces
        text = re.sub(r"[_\-.]", " ", text)

        # Remove brackets
        text = re.sub(r"[()\[\]{}]", " ", text)

        # Remove special characters
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

        # Lowercase
        text = text.lower()

        # Remove duplicate spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()