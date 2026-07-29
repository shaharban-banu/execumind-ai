"""
validator.py

Validates the canonical dataset before loading.
"""

from __future__ import annotations

from utils.logger import logger

from ingestion.models.canonical import CanonicalDataset


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

        Verifies that all canonical tables contain the required
        columns, valid primary keys, and no duplicate primary key
        values before loading into the application database.

        Args:
            canonical_dataset: Canonical dataset to validate.

        Returns:
            A tuple containing:
                - True if validation succeeds, otherwise False.
                - List of validation error messages.

        Raises:
            RuntimeError: If dataset validation fails unexpectedly.
        """

        logger.info("Starting dataset validation...")

        try:

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
        except Exception as exc:
            logger.exception(
                "Dataset validation failed: %s",
                exc,
            )
            raise RuntimeError(
                "Canonical dataset validation failed."
            ) from exc

    def _validate_table(
        self,
        table,
    ) -> list[str]:
        """
        Validate a single canonical table.

        Checks required columns, primary key existence,
        NULL primary key values, and duplicate primary keys.

        Args:
            table: Canonical table to validate.

        Returns:
            List of validation error messages.
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