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

LOAD_ORDER = [
    "customers",
    "products",
    "sellers",
    "orders",
    "payments",
    "order_items",
    "reviews",
    "deliveries",
]


class Loader:
    """
    Loads the canonical dataset into the database.

    """

    def load(self,canonical_dataset: CanonicalDataset,user_id:int) :
        """
        Persist the canonical dataset.

        Iterates through each canonical table, maps it to the
            corresponding SQLAlchemy ORM model, and persists the records
            within a single database transaction.
        
            Args:
                canonical_dataset: Canonical dataset containing the
                    transformed tables to be loaded.
        
            Returns:
                None.
        
            Raises:
                RuntimeError: If loading the dataset into the database fails.
        """

        logger.info("Loading canonical dataset into database...")

        session: Session = SessionLocal()

        try:

            table_lookup = {
                table.name: table
                for table in canonical_dataset.tables
            }

            for table_name in LOAD_ORDER:

                table = table_lookup.get(table_name)

                if table is None:
                    continue

                model = MODEL_MAPPING.get(table_name)

                if model is None:

                    logger.warning(
                        "No ORM model found for '%s'. Skipping.",
                        table_name,
                    )

                    continue

                logger.info(
                    "Loading table '%s'...",
                    table_name,
                )

                self._load_table(
                    session=session,
                    dataframe=table.dataframe,
                    model=model,
                    user_id=user_id,
                )

            session.commit()

            logger.info("Database loading completed.")

        except Exception as exc:
            session.rollback()

            logger.exception(
                "Failed to load canonical dataset: %s",
                exc,
            )

            raise RuntimeError(
                "Database loading failed."
            ) from exc

        finally:

            session.close()

    @staticmethod
    def _load_table(session: Session,dataframe,model,user_id:int) -> None:

        """
        Persist a single canonical table.

        Converts each row in the DataFrame into an ORM model instance,
        filters unsupported columns, replaces missing values with
        ``None``, and performs a bulk insert.

        Args:
            session: Active SQLAlchemy database session.
            dataframe: Canonical table data.
            model: SQLAlchemy ORM model associated with the table.

        Returns:
            None.
        """

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

        if "user_id" in valid_columns:
            cleaned["user_id"] = user_id    

            objects.append(model(**cleaned))

        session.bulk_save_objects(objects)

        logger.info(
            "Inserted %d records into '%s'.",
            len(objects),
            model.__tablename__,
        )