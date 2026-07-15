"""
relationship_detector.py

Detects relationships between canonical business entities.
"""

from __future__ import annotations

import logging

from ingestion.mappings.relationship_rules import RELATIONSHIP_RULES
from ingestion.models.dataset import DatasetMetadata
from ingestion.models.tables import Relationship

logger = logging.getLogger(__name__)


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
        Detect foreign-key relationships between tables.
        """

        logger.info("Starting relationship detection...")

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
        # Group canonical columns by table
        #
        # {
        #   "orders": {
        #       "customer_id": "buyer_id",
        #       "order_id": "sales_no"
        #   }
        # }
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

    @staticmethod
    def _calculate_confidence(
        child_table,
        child_column: str,
        parent_table,
        parent_column: str,
    ) -> float:
        """
        Calculate confidence using datatype compatibility
        and value overlap.
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