"""
capability_detector.py

Determines which business capabilities are supported by the
canonical dataset.
"""

from __future__ import annotations

from utils.logger import logger

from ingestion.mappings.field_types import ENTITY_FIELDS
from ingestion.models.canonical import (
    CanonicalDataset,
    DatasetCapabilities,
)



ENTITY_CAPABILITIES = {
    "customers": [
        "customer_analytics",
    ],
    "orders": [
        "order_analytics",
        "sales_analytics",
    ],
    "products": [
        "product_analytics",
    ],
    "payments": [
        "payment_analytics",
        "revenue_analytics",
    ],
    "reviews": [
        "review_analytics",
        "sentiment_analysis",
    ],
    "delivery": [
        "delivery_analytics",
    ],
    "sellers": [
        "seller_analytics",
    ],
}


class CapabilityDetector:
    """
    Determines which business capabilities are supported
    by the canonical dataset.
    """

    def detect(
        self,
        canonical_dataset: CanonicalDataset,
    ) -> DatasetCapabilities:
        """
        Detect business capabilities supported by the canonical dataset.

        Evaluates the canonical dataset against the required entity schema
        and determines which business capabilities can be supported based
        on the availability of mandatory entities and fields.

        Args:
            canonical_dataset: Canonical dataset to evaluate.

        Returns:
            DatasetCapabilities containing the supported capabilities,
            supported entities, missing entities, and overall coverage.

        Raises:
            RuntimeError: If capability detection fails.
        """

        logger.info("Detecting dataset capabilities...")

        try:
            capabilities = DatasetCapabilities()

            supported_entities: list[str] = []
            missing_entities: list[str] = []

            total_entities = len(ENTITY_FIELDS)

            for entity_name, fields in ENTITY_FIELDS.items():
                logger.debug(
                    "Evaluating entity '%s'.",
                    entity_name,
                )
                table = next(
                    (
                        table
                        for table in canonical_dataset.tables
                        if table.name == entity_name
                    ),
                    None,
                )

                if table is None:
                    missing_entities.append(entity_name)
                    continue

                table_columns = {
                    column.name
                    for column in table.columns
                }

                required_fields = {
                    field.name
                    for field in fields
                    if field.required
                }

                if not required_fields.issubset(table_columns):
                    missing_entities.append(entity_name)
                    continue

                supported_entities.append(entity_name)

                for capability in ENTITY_CAPABILITIES.get(entity_name, []):
                    capabilities.capabilities[capability] = True

            capabilities.supported_entities = supported_entities
            capabilities.missing_entities = missing_entities

            capabilities.coverage = round(
                len(supported_entities) / total_entities,
                2,
            )

            logger.info(
                "Detected %d capabilities.",
                len(capabilities.capabilities),
            )
            logger.debug(
                "Supported entities: %s",
                supported_entities,
            )

            logger.debug(
                "Missing entities: %s",
                missing_entities,
            )

            return capabilities
        except Exception as exc:
            logger.exception(
                "Capability detection failed: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to detect dataset capabilities."
            ) from exc