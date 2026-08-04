from pathlib import Path
import shutil

from utils.logger import logger


class PlatformResetService:

   # DATABASE = Path("data/sqlite/execumind.db")

    MODEL_DIR = Path("forecast/models")
    REPORT_DIR = Path("forecast/reports")

    VECTOR_DIR = Path("data/vectorstore")

    def reset(self):
        logger.info("Resetting platform...")

        # # Database
        # if self.DATABASE.exists():
        #     logger.info("Removing database...")
        #     self.DATABASE.unlink()

        # Forecast models
        if self.MODEL_DIR.exists():
            for file in self.MODEL_DIR.glob("*.pkl"):
                logger.info("Removing model %s", file.name)
                file.unlink()

        # Forecast reports
        if self.REPORT_DIR.exists():
            for file in self.REPORT_DIR.glob("*_metrics.json"):
                logger.info("Removing report %s", file.name)
                file.unlink()

        # Vector store
        if self.VECTOR_DIR.exists():
            logger.info("Removing vector store...")
            shutil.rmtree(self.VECTOR_DIR)

        logger.info("Platform reset completed.")