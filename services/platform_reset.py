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

    def factory_reset(self):
        """
        Completely reset platform data and generated artifacts.

        Deletes:
        - PostgreSQL processed data
        - Uploaded datasets
        - Knowledge documents
        - FAISS vector store
        - Forecast models
        - Forecast reports

        Authentication/user data is preserved.
        """

        logger.info("Starting factory reset...")

        # 1. Clear PostgreSQL processed data
        self._clear_postgres_data()

        # 2. Delete uploaded datasets
        self._clear_directory(Path("data/dataset"))

        # 3. Delete knowledge documents
        self._clear_knowledge_documents()

        # 4. Delete forecast models
        self._clear_forecast_models()

        # 5. Delete forecast reports
        self._clear_forecast_reports()

        # 6. Delete FAISS vector store
        self._clear_vector_store()

        logger.info("Factory reset completed successfully.")

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

    def _clear_directory(self, directory: Path):
        """
        Delete all files and subdirectories inside a directory,
        while keeping the directory itself.
        """

        if not directory.exists():
            return

        for item in directory.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                logger.info("Removing file: %s", item)
                item.unlink()


    def _clear_knowledge_documents(self):
        """
        Delete uploaded knowledge documents.

        Adjust the directory if your knowledge upload service
        uses a different storage location.
        """

        knowledge_dir = Path("data/uploads")

        if knowledge_dir.exists():
            self._clear_directory(knowledge_dir)