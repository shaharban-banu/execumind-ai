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

        Args:
            dataset: Scanned dataset metadata.

        Returns:
            Updated DatasetMetadata.
        """

        logger.info("Starting schema analysis.")

        for table in dataset.tables:
            self._analyze_table(table)

        logger.info("Schema analysis completed.")

        return dataset

    def _analyze_table(self, table: TableMetadata) -> None:
        """
        Analyze one table.
        """

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

    def _analyze_column(self,dataframe: pd.DataFrame,column_name: str,):
        """
        Analyze a single column.
        """

        series = dataframe[column_name]

        return ColumnMetadata(
            name=column_name,
            data_type=str(series.dtype),
            null_percentage=round(series.isna().mean() * 100, 2),
            unique_count=int(series.nunique(dropna=True)),
            sample_values=self._sample_values(series),
        )

    def _sample_values(self,series: pd.Series,) :
        """
        Return representative non-null sample values.
        """

        values = (
            series.dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        return values[: self.SAMPLE_SIZE]