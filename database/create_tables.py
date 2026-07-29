"""
Database Initialization Script.

Creates all database tables defined in the SQLAlchemy ORM models.
This script should be executed once during application setup or
whenever the database schema needs to be initialized.
"""
from database.database import engine
from database.models import Base
from utils.logger import logger

def main():

    """
    Create all database tables.

    Raises:
        RuntimeError: If table creation fails.
    """

    logger.info("Creating database tables.")

    try:

        Base.metadata.create_all(bind=engine,checkfirst=True )

        logger.info("Database tables created successfully.")

    except Exception as exc:
            logger.exception(
                "Failed to create database tables: %s",
                exc,
            )
            raise RuntimeError(
                "Database initialization failed."
            ) from exc

if __name__=="__main__":
     main()