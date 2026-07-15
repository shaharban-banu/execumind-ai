"""
loader.py

Loads the canonical dataset into the application database
using SQLAlchemy ORM.
"""
from __future__ import annotations
from utils.logger import logger
import pandas as pd
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import (
    Customer,
    Order,
    OrderItem,
    Payment,
    Product,
    Review,
    Seller,
    Delivery    
)
from ingestion.models.canonical import CanonicalDataset



MODEL_MAPPING = {
    "customers": Customer,
    "orders": Order,
    "products": Product,
    "payments": Payment,
    "reviews": Review,
    "sellers": Seller,
    "order_items": OrderItem,
    "deliveries": Delivery,
 
}


class Loader:
    """
    Loads the canonical dataset into the database.
    """

    def load(self,canonical_dataset: CanonicalDataset,) :
        """
        Persist the canonical dataset.
        """

        logger.info("Loading canonical dataset into database...")

        session: Session = SessionLocal()

        try:

            for table in canonical_dataset.tables:

                model = MODEL_MAPPING.get(table.name)

                if model is None:

                    logger.warning(
                        "No ORM model found for '%s'. Skipping.",
                        table.name,
                    )

                    continue

                logger.info(
                    "Loading table '%s'...",
                    table.name,
                )

                self._load_table(
                    session=session,
                    dataframe=table.dataframe,
                    model=model,
                )

            session.commit()

            logger.info("Database loading completed.")

        except Exception:

            session.rollback()

            logger.exception("Failed to load dataset.")

            raise

        finally:

            session.close()

    @staticmethod
    def _load_table(session: Session,dataframe,model,) -> None:

        # print("\n==============================")
        # print(model.__tablename__)
        # print(dataframe.dtypes)
        # if "order_date" in dataframe.columns:
        #     print(dataframe[["order_date"]].head())
        # print("==============================")

        records = dataframe.to_dict(orient="records")

        objects = []

        valid_columns = set(model.__table__.columns.keys())

        for record in records:

            cleaned = {}

            for key, value in record.items():

                if key not in valid_columns:
                    continue

                if pd.isna(value):
                    value = None

                cleaned[key] = value

            objects.append(model(**cleaned))

        session.bulk_save_objects(objects)