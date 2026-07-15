"""
similarity.py

Provides string similarity utilities using RapidFuzz.
"""

from rapidfuzz import fuzz, process


class SimilarityCalculator:
    """
    Utility methods for RapidFuzz string matching.
    """

    @staticmethod
    def similarity(
        text1: str,
        text2: str,
    ) -> float:
        """
        Compute similarity between two strings.

        Returns:
            Similarity score between 0 and 1.
        """

        return fuzz.ratio(text1, text2) / 100

    @staticmethod
    def best_match(
        query: str,
        candidates: list[str],
    ) -> tuple[str | None, float]:
        """
        Find the closest matching candidate.

        Returns:
            (candidate, similarity_score)
        """

        if not candidates:
            return None, 0.0

        result = process.extractOne(
            query,
            candidates,
            scorer=fuzz.ratio,
        )

        if result is None:
            return None, 0.0

        match, score, _ = result

        return match, score / 100