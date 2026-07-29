"""
customer_date_deriver.py

Derives customer_created_date for canonical customers.
"""

from __future__ import annotations

import pandas as pd

from utils.logger import logger
from ingestion.models.canonical import CanonicalDataset


class CustomerDateDeriver:
    """
    Derive customer_created_date for customer forecasting.
    """

    def derive(
        self,
        canonical_dataset: CanonicalDataset,
    ) -> CanonicalDataset:
        logger.info("Running CustomerDateDeriver...")

        customers = None
        orders = None

        for table in canonical_dataset.tables:

            if table.name == "customers":
                customers = table

            elif table.name == "orders":
                orders = table

        # No customers table
        if customers is None:
            return canonical_dataset

        customer_df = customers.dataframe

        # ----------------------------------------
        # Already available
        # ----------------------------------------

        if (
            "customer_created_date" in customer_df.columns
            and customer_df["customer_created_date"].notna().any()
        ):

            logger.info(
                "customer_created_date already available."
            )

            return canonical_dataset

        # ----------------------------------------
        # Cannot derive
        # ----------------------------------------

        if orders is None:

            logger.warning(
                "Orders table not found. "
                "Unable to derive customer_created_date."
            )

            return canonical_dataset

        order_df = orders.dataframe
        logger.info("Orders columns: %s", order_df.columns.tolist())
        logger.info("Orders rows: %d", len(order_df))

        # ----------------------------------------
        # Determine join key
        # ----------------------------------------

        if (
            "customer_master_id" in customer_df.columns
            and "customer_master_id" in order_df.columns
        ):
            join_key = "customer_master_id"

        elif (
            "customer_id" in customer_df.columns
            and "customer_id" in order_df.columns
        ):
            join_key = "customer_id"

        else:
            logger.warning(
                "No common customer key found between customers and orders."
            )
            return canonical_dataset

        # ----------------------------------------
        # Validate required columns
        # ----------------------------------------

        required = {join_key, "order_date"}

        if not required.issubset(order_df.columns):
            logger.warning(
                "Orders table missing required columns."
            )
            return canonical_dataset

        # ----------------------------------------
        # Derive first purchase date
        # ----------------------------------------

        first_orders = (
            order_df.groupby(join_key)["order_date"]
            .min()
            .reset_index()
            .rename(
                columns={
                    "order_date": "customer_created_date"
                }
            )
        )

        customer_df = customer_df.merge(
            first_orders,
            on=join_key,
            how="left",
            suffixes=("", "_derived"),
        )

        logger.info(
            "Filled customer_created_date: %d",
            customer_df["customer_created_date"].notna().sum(),
        )

        logger.info(
            "\n%s",
            customer_df[
                ["customer_master_id", "customer_created_date"]
            ].head(10)
        )

        if "customer_created_date_derived" in customer_df.columns:

            customer_df["customer_created_date"] = (
                customer_df["customer_created_date"]
                .fillna(
                    customer_df["customer_created_date_derived"]
                )
            )

            customer_df.drop(
                columns=["customer_created_date_derived"],
                inplace=True,
            )

        customers.dataframe = customer_df

        logger.info(
            "Derived customer_created_date from first order."
        )

        logger.info(
            "Filled customer_created_date: %d",
            customer_df["customer_created_date"].notna().sum()
        )

        return canonical_dataset