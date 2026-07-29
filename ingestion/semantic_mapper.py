"""
semantic_mapper.py

Maps dataset tables and columns to the canonical business schema.
"""
from __future__ import annotations
from utils.logger import logger
from ingestion.confidence import ConfidenceScorer
from ingestion.mappings.entities import BUSINESS_ENTITIES
from ingestion.mappings.field_types import ENTITY_FIELDS
from ingestion.models.dataset import DatasetMetadata
from ingestion.models.mapping import ColumnMapping, TableMapping
from ingestion.utils.embedding import EmbeddingSimilarity
from ingestion.utils.semantic_utils import SemanticUtils
from ingestion.utils.similarity import SimilarityCalculator
from ingestion.models.unmapped import UnmappedTable
from ingestion.mappings.synonyms import SYNONYMS

class SemanticMapper:
    """
    Maps uploaded dataset tables and columns to the canonical schema.
    """

    CONFIDENCE_THRESHOLD = 0.80

    def __init__(self) -> None:
        """
        Initialize the semantic mapper.

        Creates the confidence scorer used to compute hybrid
        semantic mapping confidence scores.
        """
        self.scorer = ConfidenceScorer()

    def map(self,dataset: DatasetMetadata,) -> DatasetMetadata:
        """
         Perform semantic mapping for all tables and columns.

        Maps source tables to canonical business entities and
        source columns to canonical fields using hybrid semantic
        similarity techniques.

        Args:
            dataset: Dataset metadata containing scanned tables.

        Returns:
            Updated dataset containing table and column mappings.

        Raises:
            RuntimeError: If semantic mapping fails.
        """

        logger.info("Starting semantic mapping...")

        try:

            dataset.table_mappings.clear()
            dataset.column_mappings.clear()

            # ---------------------------------------------------------
            # Score every table first
            # ---------------------------------------------------------

            candidates = []

            for table in dataset.tables:

                table_mapping = self._map_table(
                    table.table_name,
                )

                if not table_mapping.canonical_entity:
                    logger.info("Keeping unsupported table '%s' for future use.",table.table_name,)
                    dataset.unmapped_tables.append(

                        UnmappedTable(

                            table_name=table.table_name,

                            confidence=table_mapping.confidence,

                            reason="No canonical entity found",

                            suggested_entity=(
                                table_mapping.canonical_entity
                                if table_mapping.canonical_entity
                                else None
                            ),
                        )
                    )
                    continue

                candidates.append(
                    (
                        table_mapping.confidence,
                        table,
                        table_mapping,
                    )
                )

            # Highest confidence first
            candidates.sort(
                key=lambda x: x[0],
                reverse=True,
            )

            used_entities = set()

            # ---------------------------------------------------------
            # Assign canonical entities
            # ---------------------------------------------------------

            for _, table, table_mapping in candidates:

                if table_mapping.canonical_entity in used_entities:

                    logger.warning(
                        "Skipping '%s'. '%s' already assigned.",
                        table.table_name,
                        table_mapping.canonical_entity,
                    )

                    continue

                used_entities.add(
                    table_mapping.canonical_entity
                )

                dataset.table_mappings.append(
                    table_mapping
                )

                column_mappings = self._map_columns(
                    table.table_name,
                    table.columns,
                    table_mapping.canonical_entity,
                )

                dataset.column_mappings.extend(
                    column_mappings
                )

            logger.info(
                "Semantic mapping completed."
            )

            logger.debug("Order item column mappings:")

            for mapping in dataset.column_mappings:

                if mapping.source_table == "order_items":

                    print(
                        f"{mapping.source_column} -> {mapping.canonical_column}"
                    )
            return dataset
        except Exception as exc:
            logger.exception(
                "Semantic mapping failed: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to perform semantic mapping."
            ) from exc

    def _map_table(self,table_name: str,) -> TableMapping:
        """
        Map a source table to a canonical business entity.

        Args:
            table_name: Source table name.

        Returns:
            TableMapping describing the selected canonical entity.
        """

        normalized = SemanticUtils.normalize_and_replace(table_name)

        # --------------------------------------------------
        # 1. Exact alias match (highest priority)
        # --------------------------------------------------

        aliases: list[str] = []
        alias_lookup: dict[str, str] = {}

        for entity in BUSINESS_ENTITIES:

            for alias in entity.aliases:

                normalized_alias = SemanticUtils.normalize_and_replace(alias)

                aliases.append(normalized_alias)

                alias_lookup[normalized_alias] = entity.name

                if normalized == normalized_alias:

                    return TableMapping(
                        source_table=table_name,
                        canonical_entity=entity.name,
                        confidence=1.0,
                        mapping_method="alias",
                        needs_confirmation=False,
                    )

        # --------------------------------------------------
        # 2. Semantic matching
        # --------------------------------------------------

        best_match, confidence = self._find_best_match(
            normalized,
            aliases,
        )

        # --------------------------------------------------
        # 3. Reject weak matches
        # --------------------------------------------------

        if (best_match is None or confidence < self.CONFIDENCE_THRESHOLD):

            logger.warning(
                "Skipping table '%s'. No reliable entity match.",
                table_name,
            )

            return TableMapping(
                source_table=table_name,
                canonical_entity="",
                confidence=confidence,
                mapping_method="hybrid",
                needs_confirmation=True,
            )

        return TableMapping(
            source_table=table_name,
            canonical_entity=alias_lookup[best_match],
            confidence=confidence,
            mapping_method="hybrid",
            needs_confirmation=False,
        )

    def _map_columns(self,table_name: str,columns,canonical_entity: str,) -> list[ColumnMapping]:
        """
        Map source columns to canonical fields.

        Args:
            table_name: Source table name.
            columns: Source table columns.
            canonical_entity: Target canonical entity.

        Returns:
            List of column mappings.
        """

        mappings: list[ColumnMapping] = []

        fields = ENTITY_FIELDS.get(canonical_entity, [])


        field_names = []
        alias_lookup = {}

        for field in fields:

            # Canonical name
            field_names.append(field.name)
            alias_lookup[field.name] = field.name

            # Synonyms
            for alias, canonical in SYNONYMS.items():

                if canonical == field.name:

                    normalized_alias = (
                        SemanticUtils.normalize_and_replace(alias)
                    )

                    field_names.append(normalized_alias)

                    alias_lookup[normalized_alias] = field.name

                # -------------------------------------------------
                # Build all possible matches
                # -------------------------------------------------

        candidates = []

        for column in columns:

            normalized = SemanticUtils.normalize_and_replace(column.name)

            best_match, confidence = self._find_best_match(normalized,field_names,)
        
            if not best_match:
                        continue

                    # Reject weak matches
            if confidence < 0.85:
                        continue

            canonical_column = alias_lookup.get(
                        best_match,
                        best_match,
                    )

            candidates.append(
                        (
                            confidence,
                            column.name,
                            canonical_column,
                        )
                    )

                # Highest confidence first
        candidates.sort(reverse=True)

        used_source = set()
        used_target = set()

        # -------------------------------------------------
        # Greedy assignment
        # -------------------------------------------------

        for confidence, source_column, canonical_column in candidates:

            if source_column in used_source:
                continue

            if canonical_column in used_target:
                continue

            mappings.append(
                ColumnMapping(
                    source_table=table_name,
                    source_column=source_column,
                    canonical_entity=canonical_entity,
                    canonical_column=canonical_column,
                    confidence=confidence,
                    mapping_method="hybrid",
                    needs_confirmation=(
                        confidence < self.CONFIDENCE_THRESHOLD
                    ),
                )
            )

            used_source.add(source_column)
            used_target.add(canonical_column)

        return mappings

    def _find_best_match(self,text: str,candidates: list[str],) :
        """
        Find the best semantic match for a candidate string.

        Args:
            text: Source text.
            candidates: Candidate canonical values.

        Returns:
            Tuple containing the best matching candidate and its
            confidence score.
        """

        normalized_lookup = {
            SemanticUtils.normalize_and_replace(candidate): candidate
            for candidate in candidates
        }

        # Exact normalized match
        if text in normalized_lookup:
            return normalized_lookup[text], 1.0

        rapid_match, rapid_score = SimilarityCalculator.best_match(
            text,
            candidates,
        )

        embed_match, embed_score = EmbeddingSimilarity.best_match(
            text,
            candidates,
        )

        if embed_score >= rapid_score:
            best_match = embed_match
        else:
            best_match = rapid_match

        confidence = self.scorer.score(
            rapidfuzz_score=rapid_score,
            embedding_score=embed_score,
        )

        return best_match, confidence