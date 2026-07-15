"""
confidence.py

Calculates confidence scores for semantic mappings.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfidenceWeights:
    """
    Weights used when computing mapping confidence.
    """

    rapidfuzz: float = 0.35
    embedding: float = 0.40
    datatype: float = 0.15
    ontology: float = 0.10


class ConfidenceScorer:
    """
    Computes a weighted confidence score.
    """

    def __init__(
        self,
        weights: ConfidenceWeights | None = None,
    ):
        self.weights = weights or ConfidenceWeights()

    def score(
        self,
        rapidfuzz_score: float,
        embedding_score: float,
        datatype_score: float = 1.0,
        ontology_score: float = 1.0,
    ) -> float:
        """
        Compute final confidence score.
        """

        confidence = (
            rapidfuzz_score * self.weights.rapidfuzz
            + embedding_score * self.weights.embedding
            + datatype_score * self.weights.datatype
            + ontology_score * self.weights.ontology
        )

        return round(min(confidence, 1.0), 2)