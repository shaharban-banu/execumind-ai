"""
pipeline.py

End-to-end intelligent ingestion pipeline.
"""

from __future__ import annotations

import logging

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

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """
    End-to-end intelligent ingestion pipeline.
    """

    def __init__(self):

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

    def run(
        self,
        dataset_path: str,
    ):
        """
        Execute the ingestion pipeline.

        Returns
        -------
        dict
            Pipeline results.
        """

        logger.info("Starting ingestion pipeline...")

        # ----------------------------------------
        # Scan dataset
        # ----------------------------------------

        dataset = self.scanner.scan(dataset_path)

        # for table in dataset.tables:
        #     print("\n", table.table_name)
        #     print(table.dataframe.columns.tolist())
        # ----------------------------------------
        # Analyze dataset
        # ----------------------------------------

        dataset = self.analyzer.analyze(dataset)

        # ----------------------------------------
        # primary key detector
        # ----------------------------------------

        dataset = self.primary_key_detector.detect(dataset)
        
        # ----------------------------------------
        # Semantic mapping
        # ----------------------------------------

        dataset = self.semantic_mapper.map(dataset)

        # for mapping in dataset.column_mappings:
        #     if mapping.canonical_column == "customer_id":
        #          print(mapping)

        # ----------------------------------------
        # Detect relationships
        # ----------------------------------------

        dataset = self.relationship_detector.detect(dataset)

        # ----------------------------------------
        # Build canonical dataset
        # ----------------------------------------

        canonical_dataset = self.canonical_builder.build(
            dataset
        )
        # print("\nCanonical tables:")

        # for table in canonical_dataset.tables:
        #     print(table.name)

        # ----------------------------------------
        # Detect capabilities
        # ----------------------------------------

        capabilities = self.capability_detector.detect(
            canonical_dataset
        )
        canonical_dataset.capabilities = capabilities
        # ----------------------------------------
        # Transform data
        # ----------------------------------------

        canonical_dataset = self.transformer.transform(
            canonical_dataset
        )

        # ----------------------------------------
        # Validate
        # ----------------------------------------

        valid, errors = self.validator.validate(
            canonical_dataset
        )

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