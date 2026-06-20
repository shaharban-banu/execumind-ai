"""
Repository for review-related
database operations.
Load required tables from SQLite.
"""

import pandas as pd
from sqlalchemy import text

from database.database import engine
from utils.logger import logger

logger.info("Loading data from database...")


def get_reviews():
    """
    Retrieve  data from the sql table.
    """

    tables={}

    table_names=["reviews","orders","customers","order_items","products","sellers"]

    for table in table_names:
        tables[table]=pd.read_sql(f"select * from {table}",engine)

        logger.info("%s loaded :%s rows",table,len(tables[table]))
    return tables