"""Dataset validator

validates the loaded dataset before loading into SQLite."""

from utils.logger import logger
from typing import Dict
import pandas as pd
from config.settings import (TABLES,CANONICAL_TABLES,)
from etl.exceptions import DatasetValidationError

class DatasetValidator:
    def __init__(self,datasets:Dict[str,pd.DataFrame]):
        self.datasets=datasets
        self.errors=[]
    
    def validate(self):
        logger.info("starting dataset validation..........")
        self._validate_table()
        self._validate_required_columns()
        self._validate_primary_keys()
        self._validate_foreign_keys()
        self._validate_business_rules()

        if self.errors:
            message="\n".join(self.errors)
            raise DatasetValidationError(f"\n dataset validation failed :\n\n{message}")
    
    #table validation
    def _validate_table(self):
        logger.info("checking required tables...")
        for tablename,config in CANONICAL_TABLES.items():
            if not config["required"]:
                continue
            
            if  tablename not in self.datasets:
                self.errors.append(f"[TABLE] Missing required table :{tablename}")
            
    #required columns
    def _validate_required_columns(self):
        logger.info("checking required columns.....")
        for tablename,dataframe in self.datasets.items():
            schema=CANONICAL_TABLES[tablename]["columns"]
            for col,config in schema.items():
                if config["required"] and col not in dataframe.columns:
                    self.errors.append(f"[COLUMN] {tablename}.{col} is missing")

    def _validate_primary_keys(self):
        for tablename,dataframe in self.datasets.items():
            primary_keys=CANONICAL_TABLES[tablename]["primary_keys"]
            missing=[key for key in primary_keys if key not in dataframe.columns]
            if missing:
                self.errors.append(f"[PRIMARY KEY] {tablename} missing keys :{missing}")
                continue
            if dataframe[primary_keys].isnull().any().any():
                self.errors.append(f"[PRIMARY KEY] Null values found in {tablename}")
            duplicated=dataframe.duplicated(subset=primary_keys)
            if duplicated.any():
                self.errors.append(f"[PRIMARY KEY] Duplicate keys found in {tablename}")

    def _validate_foreign_keys(self):
        for tablename,dataframe in self.datasets.items():
            schema=CANONICAL_TABLES[tablename]
            foreign_keys=schema.get("foreign_keys",{})

            for fk_column,fk_info in foreign_keys.items():
                if fk_column not in dataframe.columns:
                    continue
                parent_table=fk_info["references"]["table"]
                parent_column=fk_info["references"]["column"]
                if parent_table not in self.datasets:
                    continue
                parent_df=self.datasets[parent_table]
                invalid= ~dataframe[fk_column].isin(parent_df[parent_column])
                if invalid.any():
                    count=int(invalid.sum())
                    self.errors.append(f"[FOREIGN KEY] {tablename}.{fk_column} "
                                       f"contain {count} invalid references")
                    
    def _validate_business_rules(self) -> None:

        # Payments

        if "payments" in self.datasets:

            payments = self.datasets["payments"]

            if "sales_amount" in payments.columns:

                invalid = payments["sales_amount"] < 0

                if invalid.any():

                    self.errors.append("[RULE] Negative sales_amount detected.")

        # Reviews

        if "reviews" in self.datasets:

            reviews = self.datasets["reviews"]

            if "review_score" in reviews.columns:

                invalid = ~reviews["review_score"].between(1,5,inclusive="both",)

                invalid &= reviews["review_score"].notna()

                if invalid.any():

                    self.errors.append("[RULE] review_score must be between 1 and 5.")

        # Orders

        if "orders" in self.datasets:

            orders = self.datasets["orders"]

            required = {"order_date","delivered_date",}

            if required.issubset(orders.columns):

                invalid = (orders["delivered_date"]< orders["order_date"])

                invalid &= (orders["delivered_date"].notna())

                if invalid.any():

                    self.errors.append("[RULE] delivered_date earlier than order_date.")


