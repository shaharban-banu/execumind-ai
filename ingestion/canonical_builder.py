"""
canonical_builder.py

Builds the canonical dataset from semantic mappings.
"""
from __future__ import annotations
from utils.logger import logger
import pandas as pd

from ingestion.mappings.field_types import ENTITY_FIELDS
from ingestion.models.canonical import (
    CanonicalColumn,
    CanonicalDataset,
    CanonicalTable,
)
from ingestion.models.dataset import DatasetMetadata

class CanonicalBuilder:
    """
    Builds the canonical dataset.
    """

    def build(self,dataset: DatasetMetadata,) :
        """
        Build the canonical dataset.
        """

        logger.info("Building canonical dataset...")

        canonical_dataset = CanonicalDataset()

        table_lookup = {
            table.table_name: table
            for table in dataset.tables
        }

        mappings_by_table: dict[str, list] = {}

        for mapping in dataset.column_mappings:
            mappings_by_table.setdefault(
                mapping.source_table,
                []
            ).append(mapping)

        for table_mapping in dataset.table_mappings:
            if not table_mapping.canonical_entity:
                continue
            source_table = table_lookup[
                table_mapping.source_table
            ]

            dataframe = source_table.dataframe.copy()

            column_mappings = mappings_by_table.get(
                table_mapping.source_table,
                []
            )

            rename_dict = {}
            used_canonical_columns = set()

            columns = []

            for mapping in column_mappings:

                # Prevent multiple source columns mapping to the same canonical column
                if mapping.canonical_column in used_canonical_columns:

                    logger.warning(
                        "Skipping duplicate mapping '%s' -> '%s'",
                        mapping.source_column,
                        mapping.canonical_column,
                    )
                    continue

                rename_dict[mapping.source_column] = mapping.canonical_column
                used_canonical_columns.add(mapping.canonical_column)


            logger.info("Rename mapping for table '%s':", table_mapping.source_table)

            for source, target in rename_dict.items():
                logger.info("  %s -> %s", source, target)
                
            dataframe = dataframe.rename(columns=rename_dict)
            if table_mapping.canonical_entity == "customers":
                print(dataframe.head())
            duplicates = dataframe.columns[dataframe.columns.duplicated()].tolist()

            if duplicates:
                logger.warning(
                    "Duplicate columns in '%s': %s",
                    table_mapping.source_table,
                    duplicates,
                )
            canonical_fields = ENTITY_FIELDS.get(
                table_mapping.canonical_entity,
                []
            )

            for field in canonical_fields:

                if field.name not in dataframe.columns:

                    dataframe[field.name] = None
                reverse_lookup = {v: k for k, v in rename_dict.items()}
                columns.append(
                    CanonicalColumn(
                        name=field.name,
                        data_type=field.data_type,
                        required=field.required,
                        source_table=table_mapping.source_table,
                        source_column=reverse_lookup.get(field.name),
                        mapped=field.name in rename_dict.values(),
                    )
                )
            duplicates = dataframe.columns[dataframe.columns.duplicated()].tolist()

            if duplicates:
                logger.warning(
                    "Duplicate canonical columns in %s: %s",
                    table_mapping.source_table,
                    duplicates,
                )
            canonical_table = CanonicalTable(
                name=table_mapping.canonical_entity,
                columns=columns,
                dataframe=dataframe,
                primary_keys=source_table.primary_keys,
                relationships=[
                    r for r in dataset.relationships 
                    if r.source_table==source_table.table_name
                ],
                row_count=len(dataframe),
            )

            if table_mapping.canonical_entity == "order_items":
                print("\n===== After Canonical Builder =====")
                print(dataframe.columns.tolist())
                print(dataframe.head())
            
            canonical_dataset.tables.append(canonical_table)

        logger.info(
            "Canonical dataset built successfully."
        )

        return canonical_dataset