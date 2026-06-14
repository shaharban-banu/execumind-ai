"""
Database Query Tool.

Provides controlled access to the SQLite
analytical database for MCP tools and agents.
"""
from utils.logger import logger
import pandas as pd
from sqlalchemy import text
from database.database import engine



def query_db(sql):
    """
    Execute a SQL query against the database.

    Args:
        sql:
            SQL query string.

    Returns:
        list[dict]:
            Query results.
    """
    try:
        sql_lower = sql.strip().lower()

        blocked_commands = [
                            "drop",
                            "delete",
                            "truncate",
                            "alter"
                        ]

        for command in blocked_commands:

            if sql_lower.startswith(command):

                raise ValueError(f"{command.upper()} queries are not allowed.")
            
        logger.info("Executing query : %s",sql)
        df=pd.read_sql(text(sql),engine)
        results=df.to_dict(orient="records")
        logger.info("Returned %s rows",len(results))
        return results
    except Exception:
        logger.exception("Database query failed")
        raise

#test 
if __name__=="__main__":
    query = """
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
"""
    results=query_db(query)
    print(results)
