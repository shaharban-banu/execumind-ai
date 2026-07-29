"""
relationship_detector.py

Detects relationships between canonical business entities.
"""

from __future__ import annotations

from utils.logger import logger

from ingestion.mappings.relationship_rules import RELATIONSHIP_RULES
from ingestion.models.dataset import DatasetMetadata
from ingestion.models.tables import Relationship

class RelationshipDetector:
    """
    Detect relationships between canonical entities.
    """

    CONFIDENCE_THRESHOLD = 0.80

    def detect(
        self,
        dataset: DatasetMetadata,
    ) -> DatasetMetadata:
        """
        Detect foreign-key relationships between canonical entities.

        Uses semantic mappings together with predefined business
        relationship rules to identify foreign-key relationships
        between canonical tables and assign a confidence score to
        each detected relationship.

        Args:
            dataset: Dataset metadata containing semantic mappings,
                source tables, and canonical entities.

        Returns:
            Updated dataset metadata with detected relationships.

        Raises:
            RuntimeError: If relationship detection fails.
        """

        logger.info("Starting relationship detection...")

        try:

            dataset.relationships.clear()

            # --------------------------------------------------
            # Lookup source tables
            # --------------------------------------------------

            table_lookup = {
                table.table_name: table
                for table in dataset.tables
            }

            # --------------------------------------------------
            # Lookup canonical entity for each table
            # --------------------------------------------------

            entity_lookup = {
                mapping.source_table: mapping.canonical_entity
                for mapping in dataset.table_mappings
            }

            # --------------------------------------------------
        
            # --------------------------------------------------

            column_lookup: dict[str, dict[str, str]] = {}

            for mapping in dataset.column_mappings:

                column_lookup.setdefault(
                    mapping.source_table,
                    {}
                )[mapping.canonical_column] = mapping.source_column

            # --------------------------------------------------
            # Detect relationships
            # --------------------------------------------------

            for child_table, child_entity in entity_lookup.items():

                parent_rules = RELATIONSHIP_RULES.get(
                    child_entity,
                    {}
                )

                for parent_table, parent_entity in entity_lookup.items():

                    if child_table == parent_table:
                        continue

                    # Not a valid business relationship
                    if parent_entity not in parent_rules:
                        continue

                    canonical_key = parent_rules[parent_entity]

                    child_column = (
                        column_lookup
                        .get(child_table, {})
                        .get(canonical_key)
                    )

                    parent_column = (
                        column_lookup
                        .get(parent_table, {})
                        .get(canonical_key)
                    )

                    if child_column is None or parent_column is None:
                        continue

                    confidence = self._calculate_confidence(
                        child_table=table_lookup[child_table],
                        child_column=child_column,
                        parent_table=table_lookup[parent_table],
                        parent_column=parent_column,
                    )

                    if confidence < self.CONFIDENCE_THRESHOLD:
                        continue

                    dataset.relationships.append(
                        Relationship(
                            source_table=child_table,
                            source_column=child_column,
                            target_table=parent_table,
                            target_column=parent_column,
                            canonical_column=canonical_key,
                            relationship_type="foreign_key",
                            confidence=confidence,
                        )
                    )

                    logger.info(
                        "Detected relationship: %s.%s -> %s.%s (%.2f)",
                        child_table,
                        child_column,
                        parent_table,
                        parent_column,
                        confidence,
                    )

            logger.info(
                "Relationship detection completed. %d relationships found.",
                len(dataset.relationships),
            )

            return dataset
        except Exception as exc:
            logger.exception(
                "Relationship detection failed: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to detect relationships."
            ) from exc

    @staticmethod
    def _calculate_confidence(
        child_table,
        child_column: str,
        parent_table,
        parent_column: str,
    ) -> float:
        """
        Calculate the confidence score for a detected relationship.

        The confidence score is computed using datatype compatibility
        and the overlap of values between the child and parent columns.

        Args:
            child_table: Child table metadata.
            child_column: Candidate foreign-key column.
            parent_table: Parent table metadata.
            parent_column: Candidate primary-key column.

        Returns:
            Confidence score between 0.0 and 1.0.
        """

        child_series = child_table.dataframe[child_column]
        parent_series = parent_table.dataframe[parent_column]

        # -----------------------------
        # Datatype score
        # -----------------------------

        datatype_score = (
            1.0
            if child_series.dtype == parent_series.dtype
            else 0.0
        )

        # -----------------------------
        # Value overlap
        # -----------------------------

        child_values = set(child_series.dropna())
        parent_values = set(parent_series.dropna())

        if not child_values:
            return 0.0

        overlap = len(child_values & parent_values)

        overlap_score = overlap / len(child_values)

        # -----------------------------
        # Final confidence
        # -----------------------------

        confidence = (
            datatype_score * 0.30 +
            overlap_score * 0.70
        )

        return round(min(confidence, 1.0), 2)