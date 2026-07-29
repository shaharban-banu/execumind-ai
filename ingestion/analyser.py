"""
analyzer.py

Analyzes scanned dataset tables and enriches them with
column-level metadata.

This module does not detect relationships or perform
semantic mapping.
"""
from __future__ import annotations
import pandas as pd
from utils.logger import logger
from ingestion.models.dataset import DatasetMetadata
from ingestion.models.tables import ColumnMetadata, TableMetadata

class SchemaAnalyzer:
    """
    Analyzes dataset tables and extracts metadata.
    """

    SAMPLE_SIZE = 5

    def analyze(self, dataset: DatasetMetadata) -> DatasetMetadata:
        """
        Analyze every table in a dataset.
        Extracts column-level metadata for each table and enriches the
        dataset metadata with schema information.

        Args:
            dataset: Scanned dataset metadata.

        Returns:
            Updated DatasetMetadata.
        """

        logger.info("Starting schema analysis.")

        try:
            for table in dataset.tables:
                self._analyze_table(table)

            logger.info("Schema analysis completed.")

            return dataset
        except Exception as exc:
            logger.exception(
                "Schema analysis failed: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to analyze dataset schema."
            ) from exc

    def _analyze_table(self, table: TableMetadata) -> None:
        """
        Analyze a single table.

        Extracts metadata for every column in the provided table.

        """
        logger.debug("Analyzing table '%s'.", table.table_name)

        dataframe = table.dataframe

        if dataframe is None:
            return

        columns = []

        for column in dataframe.columns:
            columns.append(
                self._analyze_column(
                    dataframe=dataframe,
                    column_name=column,
                )
            )

        table.columns = columns

    def _analyze_column(
            self,
            dataframe: pd.DataFrame,
            column_name: str,
            )-> ColumnMetadata:
        """
        Analyze a single column.

        Extracts metadata including data type, null percentage,
        unique value count, and representative sample values.

        """

        series = dataframe[column_name]

        return ColumnMetadata(
            name=column_name,
            data_type=str(series.dtype),
            null_percentage=round(series.isna().mean() * 100, 2),
            unique_count=int(series.nunique(dropna=True)),
            sample_values=self._sample_values(series),
        )

    def _sample_values(
            self,
            series: pd.Series,
            ) :
        """
        Return representative non-null sample values.

        Extracts up to ``SAMPLE_SIZE`` distinct non-null values from the
        column to assist with downstream schema mapping.

        """

        values = (
            series.dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        return values[: self.SAMPLE_SIZE]