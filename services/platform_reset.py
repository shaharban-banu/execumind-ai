from pathlib import Path
import shutil

from sqlalchemy import text

from database.database import SessionLocal
from utils.logger import logger


class PlatformResetService:

    MODEL_DIR = Path("data/models")
    REPORT_DIR = Path("data/forecast_reports")
    VECTOR_DIR = Path("data/vectorstore")

    def reset(self):
        """
        Clear generated intelligence artifacts.

        Used when uploading/replacing datasets.
        Does NOT clear PostgreSQL data.
        """
        logger.info("Resetting generated platform artifacts...")

        self._clear_forecast_models()
        self._clear_forecast_reports()
        self._clear_vector_store()

        logger.info("Generated platform artifacts reset completed.")

    def reset_for_reprocess(self):
        """
        Completely clear processed platform data while keeping:
        - uploaded datasets
        - knowledge documents

        This is used by the Reprocess Platform operation.
        """

        logger.info("Starting platform reprocess reset...")

        # 1. Clear PostgreSQL processed/business data
        self._clear_postgres_data()

        # 2. Delete generated forecast models
        self._clear_forecast_models()

        # 3. Delete generated forecast reports
        self._clear_forecast_reports()

        # 4. Delete FAISS vector store
        self._clear_vector_store()

        logger.info(
            "Platform reprocess reset completed. "
            "Datasets and knowledge documents were preserved."
        )

    def _clear_postgres_data(self):
        """
        Clear only processed/business tables.

        Authentication/user data is intentionally not touched.
        """

        db = SessionLocal()

        try:
            logger.info("Clearing PostgreSQL processed data...")

            db.execute(
                text(
                    """
                    TRUNCATE TABLE
                        
                        reviews,
                        order_items,
                        payments,
                        deliveries,
                        orders,
                        products,
                        sellers,
                        customers
                    RESTART IDENTITY CASCADE
                    """
                )
            )

            db.commit()

            logger.info("PostgreSQL processed data cleared.")

        except Exception:
            db.rollback()
            logger.exception(
                "Failed to clear PostgreSQL processed data."
            )
            raise

        finally:
            db.close()

    def _clear_forecast_models(self):
        """Delete generated forecast models."""

        if not self.MODEL_DIR.exists():
            return

        for file in self.MODEL_DIR.glob("*.pkl"):
            logger.info("Removing forecast model: %s", file.name)
            file.unlink()

    def _clear_forecast_reports(self):
        """Delete generated forecast reports."""

        if not self.REPORT_DIR.exists():
            return

        for file in self.REPORT_DIR.glob("*_metrics.json"):
            logger.info("Removing forecast report: %s", file.name)
            file.unlink()

    def _clear_vector_store(self):
        """Delete FAISS index and associated metadata."""

        if not self.VECTOR_DIR.exists():
            return

        for item in self.VECTOR_DIR.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                logger.info("Removing vector store file: %s", item.name)
                item.unlink()