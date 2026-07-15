"""
validator.py

Validates the canonical dataset before loading.
"""

from __future__ import annotations

import logging

from ingestion.models.canonical import CanonicalDataset

logger = logging.getLogger(__name__)


class Validator:
    """
    Validates canonical datasets.
    """

    def validate(
        self,
        canonical_dataset: CanonicalDataset,
    ) -> tuple[bool, list[str]]:
        """
        Validate the canonical dataset.

        Returns
        -------
        tuple
            (is_valid, validation_errors)
        """

        logger.info("Starting dataset validation...")

        errors: list[str] = []

        for table in canonical_dataset.tables:

            errors.extend(
                self._validate_table(table)
            )

        is_valid = len(errors) == 0

        if is_valid:

            logger.info("Validation successful.")

        else:

            logger.warning(
                "Validation failed with %d error(s).",
                len(errors),
            )

        return is_valid, errors

    def _validate_table(
        self,
        table,
    ) -> list[str]:
        """
        Validate a single canonical table.
        """

        errors: list[str] = []

        df = table.dataframe

        # ------------------------------------
        # Required columns
        # ------------------------------------

        for column in table.columns:

            if column.required:

                if column.name not in df.columns:

                    errors.append(
                        f"{table.name}: Missing required column '{column.name}'."
                    )

                    continue

                if df[column.name].isnull().all():

                    errors.append(
                        f"{table.name}: Required column '{column.name}' contains only null values."
                    )

        # ------------------------------------
        # Primary key validation
        # ------------------------------------

        if table.primary_keys:

            # Check every PK column exists
            for pk in table.primary_keys:

                if pk not in df.columns:

                    errors.append(
                        f"{table.name}: Primary key column '{pk}' not found."
                    )

                    return errors

            # Check NULL values in PK
            missing_pk = (
                df[table.primary_keys]
                .isnull()
                .any(axis=1)
                .sum()
            )

            if missing_pk:

                errors.append(
                    f"{table.name}: {missing_pk} rows contain NULL primary key values."
                )

            # Check duplicate PKs
            duplicate_pk = (
                df.duplicated(
                    subset=table.primary_keys
                ).sum()
            )

            if duplicate_pk:

                errors.append(
                    f"{table.name}: {duplicate_pk} duplicate primary key values found."
                )

        return errors