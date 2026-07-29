"""
primary_key_detector.py

Automatically detects primary keys for every table.
"""
from __future__ import annotations
from utils.logger import logger
from itertools import combinations
from ingestion.models.dataset import DatasetMetadata


class PrimaryKeyDetector:
    """
    Detect primary keys using data profiling.
    """

    UNIQUE_THRESHOLD = 0.98

    ID_KEYWORDS = (
        "id",
        "key",
        "code",
        "number",
        "no",
        "uuid",
    )

    def detect(self,dataset: DatasetMetadata,) -> DatasetMetadata:
        """
        Detect primary keys for every table.

        Profiles each table and identifies the most likely primary key
        columns using uniqueness, completeness, and identifier naming
        heuristics.

        Args:
            dataset: Dataset metadata containing the scanned tables.

        Returns:
            Updated dataset metadata with detected primary keys.

        Raises:
            RuntimeError: If primary key detection fails.
        """

        logger.info("Detecting primary keys...")

        try:

            for table in dataset.tables:

                table.primary_keys = self._detect_table_primary_keys(table)

                logger.info(
                    "%s -> %s",
                    table.table_name,
                    table.primary_keys,
                )

            logger.info("Primary key detection completed.")

            return dataset
        except Exception as exc:
            logger.exception(
                "Primary key detection failed: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to detect primary keys."
            ) from exc

    def _detect_table_primary_keys(self,table,) -> list[str]:
        """
        Detect the primary key for a single table.

        Attempts to identify both single-column and composite primary
        keys using data profiling heuristics.

        Args:
            table: Table metadata containing the source DataFrame.

        Returns:
            List of detected primary key column names.
        """

        df = table.dataframe

        if df is None or df.empty:
            return []

        # --------------------------
        # Step 1
        # Single-column PK
        # --------------------------

        scored = []

        for column in df.columns:

            score = self._score_column(df,column,)

            scored.append((score, column))

        scored.sort(reverse=True)

        for score, column in scored:

            if score < 0.80:
                continue

            if self._is_unique(df, [column]):
                return [column]

        # --------------------------
        # Step 2
        # Composite PK
        # --------------------------

        candidate_columns = [
            column
            for score, column in scored
            if score >= 0.50
        ]

        for size in (2, 3):

            for cols in combinations(candidate_columns,size,):

                if self._is_unique(df,list(cols),):
                    return list(cols)

        return []

    def _score_column(self,df,column: str,) -> float:
        """
        Calculate the likelihood that a column is a primary key.

        The score is based on data completeness, uniqueness, and
        identifier naming conventions.

        Args:
            df: Source DataFrame.
            column: Column name to evaluate.

        Returns:
            Confidence score between 0.0 and 1.0.
        """

        score = 0.0

        series = df[column]

        # --------------------
        # No nulls
        # --------------------

        if series.isna().sum() == 0:
            score += 0.30

        # --------------------
        # High uniqueness
        # --------------------

        uniqueness = (
            series.nunique(dropna=True)
            / max(len(series), 1)
        )

        score += uniqueness * 0.50

        # --------------------
        # Identifier name
        # --------------------

        name = column.lower()

        if any(
            keyword in name
            for keyword in self.ID_KEYWORDS
        ):
            score += 0.20

        return min(score, 1.0)

    @staticmethod
    def _is_unique(df,columns: list[str],) -> bool:
        """
        Determine whether one or more columns uniquely identify rows.

        Args:
            df: Source DataFrame.
            columns: Columns to evaluate.

        Returns:
            True if the column combination uniquely identifies every row;
            otherwise, False.
        """

        if df[columns].isna().any().any():
            return False

        return not df.duplicated(
            subset=columns,
        ).any()