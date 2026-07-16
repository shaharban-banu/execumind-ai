"""
transformer.py

Transforms canonical tables into a standardized format.
"""

from __future__ import annotations

from utils.logger import logger
import pandas as pd
from ingestion.models.canonical import CanonicalColumn, CanonicalDataset

class Transformer:
    """
    Performs transformations on the canonical dataset.
    """

    def transform(self,canonical_dataset: CanonicalDataset,) -> CanonicalDataset:
        """
        Transform every canonical table.
        """

        logger.info("Starting data transformation...")

        for table in canonical_dataset.tables:

            logger.info("Transforming table: %s",table.name,)

            df = table.dataframe.copy()

            df = self._trim_strings(df)

            df = self._convert_datatypes(df,table.columns,)

            df = self._normalize_quantity(table.name, df)

            df = self._generate_derived_fields(table.name, df)
            
            df = self._generate_missing_ids(table.name,df,)

            df = self._fill_missing_customer_master_id(table.name, df)

            df = self._normalize_booleans(df)

            df = self._replace_empty_strings(df)

            df = self._replace_nan_with_none(df)

            df = self._remove_duplicates(df,table.primary_keys,)

            df = self._handle_missing_values(df,table.columns,)

            df = self._create_features(df,)

            if table.name=="reviews":
                df=self._create_review_text(df)

            table.dataframe = df
            table.row_count=len(df)

        logger.info("Data transformation completed.")

        return canonical_dataset
    
    @staticmethod
    def _trim_strings(df: pd.DataFrame) -> pd.DataFrame:
        """
        Trim whitespace from string columns.
        """
        
        object_columns = df.select_dtypes(include=["object","string"]).columns

        for column in object_columns:

            #print(f"\nProcessing column: {column}")

            value = df[column]

            #print("Type:", type(value))

            if isinstance(value, pd.DataFrame):
                print("Duplicate column detected!")
                print(value.columns.tolist())
                raise ValueError(f"Duplicate column name: {column}")

            df[column] = value.astype(str).str.strip()

        return df

    @staticmethod
    def _convert_datatypes(df: pd.DataFrame,columns: list[CanonicalColumn],) :
        """
        Convert dataframe columns using canonical metadata.
        """
        #print("\nColumn metadata")

        for column in columns:

            #print(column.name, "->", column.data_type)

            if column.name not in df.columns:
                continue

            try:

                if column.data_type == "datetime":

                    df[column.name] = pd.to_datetime(
                        df[column.name],
                        errors="coerce",
                    )

                elif column.data_type == "integer":

                    df[column.name] = pd.to_numeric(
                        df[column.name],
                        errors="coerce",
                    ).astype("Int64")

                elif column.data_type == "float":

                    df[column.name] = pd.to_numeric(
                        df[column.name],
                        errors="coerce",
                    )

                elif column.data_type == "boolean":

                    df[column.name] = (
                        df[column.name]
                        .astype(str)
                        .str.lower()
                        .map(
                            {
                                "true": True,
                                "false": False,
                                "yes": True,
                                "no": False,
                                "y": True,
                                "n": False,
                                "1": True,
                                "0": False,
                            }
                        )
                    )

                else:

                    df[column.name] = (
                        df[column.name]
                        .astype("string")
                        
                    )

            except Exception as exc:

                logger.warning(
                    "Failed to convert column '%s': %s",
                    column.name,
                    exc,
                )

        return df

    @staticmethod
    def _normalize_booleans(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize boolean-like object columns.
        """

        boolean_map = {
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
            "y": True,
            "n": False,
            "1": True,
            "0": False,
        }

        object_columns = df.select_dtypes(include=["object","string"]).columns

        for column in object_columns:

            values = (
                df[column]
                .dropna()
                .astype(str)
                .str.lower()
                .unique()
            )

            if len(values) == 0:
                continue

            if set(values).issubset(boolean_map.keys()):

                df[column] = (
                    df[column]
                    .astype(str)
                    .str.lower()
                    .map(boolean_map)
                )

        return df

    @staticmethod
    def _replace_empty_strings(df: pd.DataFrame,) -> pd.DataFrame:
        """
        Replace empty strings with None.
        """

        df.replace("",None,inplace=True,)

        return df
    @staticmethod
    def _replace_nan_with_none(df):

        return df.where(df.notna(), None)
    

    @staticmethod
    def _generate_missing_ids(
        table_name: str,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate canonical IDs when the source dataset
        does not provide them.
        """

        if table_name == "payments":

            if (
                "payment_id" in df.columns
                and df["payment_id"].isna().all()
            ):

                if "payment_sequence" in df.columns:

                    df["payment_id"] = (
                        df["order_id"].astype(str)
                        + "_"
                        + df["payment_sequence"].astype(str)
                    )

                else:

                    df["payment_id"] = [
                        f"PAY_{i+1:08d}"
                        for i in range(len(df))
                    ]

        return df
    
    @staticmethod
    def _remove_duplicates(df: pd.DataFrame,primary_keys: list[str],) -> pd.DataFrame:
        """
        Remove duplicate rows using detected primary keys.
        """

        if primary_keys:

            before = len(df)

            df = df.drop_duplicates(subset=primary_keys,)

            removed = before - len(df)

            if removed:

                logger.info("Removed %d duplicate rows.",removed,)

        else:

            df = df.drop_duplicates()

        return df

    @staticmethod
    def _handle_missing_values(
        df: pd.DataFrame,
        columns: list[CanonicalColumn],
    ) -> pd.DataFrame:
        """
        Generic missing-value handling.
        """

        for column in columns:

            if column.name not in df.columns:
                continue

            series = df[column.name]

            if column.data_type == "string":

                df[column.name] = series.fillna("")

            elif column.data_type in (
                "integer",
                "float",
            ):

                if series.notna().any():

                    median = series.median()

                    df[column.name] = (
                        series.fillna(median)
                    )

        return df

    @staticmethod
    def _create_features(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create generic derived features.
        """

        if "order_date" in df.columns:

            df["order_year"] = (
                df["order_date"].dt.year
            )

            df["order_month"] = (
                df["order_date"].dt.month
            )

            df["order_quarter"] = (
                df["order_date"].dt.quarter
            )

        if (
            "order_date" in df.columns
            and "delivered_date" in df.columns
        ):

            df["delivery_days"] = (
                df["delivered_date"]
                - df["order_date"]
            ).dt.days

        if (
            "price" in df.columns
            and "quantity" in df.columns
        ):

            df["total_amount"] = (
                df["price"]
                * df["quantity"]
            )

        return df
    
    @staticmethod
    def _create_review_text(df: pd.DataFrame) -> pd.DataFrame:
        """
        Combine review title and review comment into one
        searchable text field.
        """

        title = (
            df["review_title"]
            if "review_title" in df.columns
            else ""
        )

        comment = (
            df["review_comment"]
            if "review_comment" in df.columns
            else ""
        )

        df["review_text"] = (
            title.fillna("").astype(str)
            + "\n"
            + comment.fillna("").astype(str)
        ).str.strip()

        return df
    
    @staticmethod
    def _fill_missing_customer_master_id(
        table_name: str,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        If the dataset doesn't provide a customer_master_id,
        fall back to customer_id.
        """

        if table_name != "customers":
            return df

        if (
            "customer_master_id" in df.columns
            and "customer_id" in df.columns
        ):
            df["customer_master_id"] = (
                df["customer_master_id"]
                .fillna(df["customer_id"])
            )

        return df
    @staticmethod
    def _normalize_quantity(
        table_name: str,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Ensure every order item has a quantity.
        If quantity is missing, assume 1.
        """

        if table_name != "order_items":
            return df

        if "quantity" not in df.columns:
            df["quantity"] = 1

        else:
            df["quantity"] = df["quantity"].fillna(1)

        return df
    
    @staticmethod
    def _generate_derived_fields(
        table_name: str,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Generate canonical derived fields.
        """

        if table_name == "order_items":

            if (
                "order_item_value" in df.columns
                and "unit_price" in df.columns
            ):

                missing = df["order_item_value"].isna()

                df.loc[missing, "order_item_value"] = (
                    df.loc[missing, "unit_price"]
                    * df.loc[missing, "quantity"]
                )

        return df
            

