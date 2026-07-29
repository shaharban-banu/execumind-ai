"""
pipeline.py

End-to-end intelligent ingestion pipeline.
"""

from __future__ import annotations

from utils.logger import logger

from ingestion.analyser import SchemaAnalyzer
from ingestion.canonical_builder import CanonicalBuilder
from ingestion.capability_detector import CapabilityDetector
from ingestion.loader import Loader
from ingestion.relationship_detector import RelationshipDetector
from ingestion.scanner import DatasetScanner
from ingestion.semantic_mapper import SemanticMapper
from ingestion.transformer import Transformer
from ingestion.validator import Validator
from ingestion.primary_key_detector import PrimaryKeyDetector
from ingestion.customer_date_deriver import CustomerDateDeriver


class IngestionPipeline:
    """
    End-to-end intelligent ingestion pipeline.
    """

    def __init__(self):
        """
        Initialize the ingestion pipeline.

        Creates and configures all pipeline components required to scan,
        analyse, map, transform, validate, and load datasets into the
        application database.
        """

        self.scanner = DatasetScanner()
        self.analyzer = SchemaAnalyzer()
        self.semantic_mapper = SemanticMapper()
        self.relationship_detector = RelationshipDetector()
        self.canonical_builder = CanonicalBuilder()
        self.capability_detector = CapabilityDetector()
        self.transformer = Transformer()
        self.validator = Validator()
        self.loader = Loader()
        self.primary_key_detector=PrimaryKeyDetector()
        self.customer_date_deriver = CustomerDateDeriver()

    def run(
        self,
        dataset_path: str,
    ):
        """
        Execute the end-to-end ingestion pipeline.

        The pipeline scans the dataset, analyses its schema, detects
        primary keys and relationships, performs semantic mapping,
        constructs the canonical dataset, detects supported business
        capabilities, transforms and validates the data, and finally
        loads the validated dataset into the application database.

        Args:
            dataset_path: Path to the source dataset.

        Returns:
            Dictionary containing the pipeline execution status,
            detected capabilities, relationships, canonical tables,
            and any unmapped tables.

        Raises:
            RuntimeError: If any stage of the ingestion pipeline fails.
        """

        logger.info("Starting ingestion pipeline...")

        try:

            # ----------------------------------------
            # Scan dataset
            # ----------------------------------------

            dataset = self.scanner.scan(dataset_path)
            logger.info("Dataset scanning completed.")

            # ----------------------------------------
            # Analyze dataset
            # ----------------------------------------

            dataset = self.analyzer.analyze(dataset)
            logger.info("Schema analysis completed.")

            # ----------------------------------------
            # primary key detector
            # ----------------------------------------

            dataset = self.primary_key_detector.detect(dataset)
            logger.info("Primary key detection completed.")
            
            # ----------------------------------------
            # Semantic mapping
            # ----------------------------------------

            dataset = self.semantic_mapper.map(dataset)
            logger.info("Semantic mapping completed.")

            # ----------------------------------------
            # Detect relationships
            # ----------------------------------------

            dataset = self.relationship_detector.detect(dataset)
            logger.info("Relationship detection completed.")

            # ----------------------------------------
            # Build canonical dataset
            # ----------------------------------------

            canonical_dataset = self.canonical_builder.build(
                dataset
            )
            logger.info("Canonical dataset construction completed.")

            canonical_dataset = (
                self.customer_date_deriver.derive(
                    canonical_dataset
                )
            )
            # ----------------------------------------
            # Detect capabilities
            # ----------------------------------------

            capabilities = self.capability_detector.detect(
                canonical_dataset
            )
            canonical_dataset.capabilities = capabilities
            logger.info("Capability detection completed.")
            # ----------------------------------------
            # Transform data
            # ----------------------------------------

            canonical_dataset = self.transformer.transform(
                canonical_dataset
            )
            logger.info("Data transformation completed.")

            # ----------------------------------------
            # Validate
            # ----------------------------------------

            valid, errors = self.validator.validate(
                canonical_dataset
            )
            logger.info("Dataset validation completed.")

            if not valid:

                logger.error(
                    "Validation failed."
                )

                return {
                    "success": False,
                    "errors": errors,
                }

            # ----------------------------------------
            # Load into database
            # ----------------------------------------

            self.loader.load(
                canonical_dataset
            )

            logger.info(
                "Ingestion pipeline completed successfully."
            )

            return {
                "success": True,
                "capabilities": canonical_dataset.capabilities,
                "relationships": dataset.relationships,
                "tables": [
                    table.name
                    for table in canonical_dataset.tables
                ],
                "unmapped_tables": [
                    {
                        "table": table.table_name,
                        "confidence": table.confidence,
                        "reason": table.reason,
                        "suggested_entity": table.suggested_entity,
                    }

                    for table in dataset.unmapped_tables
                ],
            }
        except Exception as exc:
            logger.exception(
                "Ingestion pipeline failed: %s",
                exc,
            )
            raise RuntimeError(
                "Ingestion pipeline execution failed."
            ) from exc