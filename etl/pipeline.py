"""
ETL Pipeline for ExecuMind AI.
"""
from utils.logger import logger
from database.database import SessionLocal
from connectors.connector_factory import get_connector
from etl.schema_mapper import SchemaMapper
from etl.transform import DataTransformer
from etl.validator import DatasetValidator
from etl.load import DataLoader

class ETLPipeline:
    def run(self):
        logger.info("="*50)
        logger.info("Starting Execumind ETL pipeline")
        logger.info("="*50)

        session=SessionLocal()
        try:
            #extract
            connector=get_connector()
            datasets=connector.load_tables()

            #schema mapping
            datasets=SchemaMapper(datasets).map()

            #transform
            datasets=DataTransformer(datasets).transform()

            #validate
            DatasetValidator(datasets).validate()

            #load
            DataLoader(session,datasets).load()

            logger.info("ETL pipeline completed successfully")
        except Exception as e:
            session.rollback()
            logger.error(type(e).__name__)
            logger.error(str(e))
            # logger.error("ETL pipeline failed: %s", e)
            raise
        finally:
            session.close()

