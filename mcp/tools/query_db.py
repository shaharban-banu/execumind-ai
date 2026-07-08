"""
Database Query Tool.

Provides controlled access to the SQLite
analytical database for MCP tools and agents.
Supports two modes:
    historical  — queries original olist tables (default)
    live        — queries live mirror tables populated
                  by the data simulator
 
Agents never need to know which mode they are in.
FastAPI sets the mode based on whether the simulator
is running.
"""
from utils.logger import logger
import pandas as pd
from sqlalchemy import text
from database.database import engine
from config.settings import (BLOCKED_SQL_COMMANDS,LIVE_TABLE_MAPPING)
import re

 
# Tables that are always static — never replaced
# even in live mode. Agents join to these directly.
_STATIC_TABLES = {
    "customers",
    "sellers",
    "products",
    "geolocation",
    "category_translations",
}
 
# --------------------------------------------------
# Internal helpers
# --------------------------------------------------
 
def _apply_live_mode(sql: str) -> str:
    """
    Replace historical table names with live mirror names.
 
    Only swaps the four streaming tables. Static reference
    tables (customers, sellers, products, geolocation) are
    always queried from the originals.
 
    Args:
        sql:
            Original SQL query referencing historical tables.
 
    Returns:
        SQL with live mirror table names substituted.
    """
    sql_rewritten = sql
 
    for historical, live in LIVE_TABLE_MAPPING.items():
        # Use word-boundary-safe replacement:
        # replace " orders " but not " live_orders "
        # Simple approach: replace table name when followed
        # by space, newline, comma, or end of string
        
        pattern = rf"\b{historical}\b"
        sql_rewritten = re.sub(pattern, live, sql_rewritten)
 
    return sql_rewritten
 
 
def _validate_sql(sql: str) -> None:
    """
    Allow only SELECT queries.
    """
    sql_lower = sql.strip().lower()
 
    for command in BLOCKED_SQL_COMMANDS:
        if command in sql_lower:
            raise ValueError(
                f"Blocked SQL command detected: "
                f"{command.strip().upper()}. "
                f"Only SELECT queries are permitted."
            )
 

def query_db(sql:str,mode:str="historical"):
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
        _validate_sql(sql)
        if mode=="live":
            effective_sql=_apply_live_mode(sql)
            logger.info("Live mode — rewritten SQL: %s",effective_sql)
        else:
            effective_sql=sql
            logger.info("Historical mode — SQL: %s",effective_sql)

        df=pd.read_sql(text(effective_sql),engine)
        results=df.to_dict(orient="records")
       
        logger.info("Returned %s rows [mode=%s]",len(results),mode)
        return results
    except ValueError:
        raise
    except Exception:
        logger.exception("Database query failed [mode=%s] SQL:%s",mode,sql)
        raise

#test 
if __name__=="__main__":
    #Historical mode
    print("\n-------HISTORICAL MODE-------")
    query = """
        SELECT
            order_status,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY order_status
        """
    results=query_db(query)
    for row in results:
        print(row)

    #Live mode
    print("\n------LIVE MODE-------")
    query = """
        SELECT
            COUNT(*) AS total_live_orders
        FROM orders
        """
    results=query_db(query,mode="live")
    for row in results:
        print(row)

    #test security
    print("\n------Security Check------")
    try:
        query_db("SELECT * FROM orders; DROP TABLE orders")
    except ValueError as e:
        print(f"Blocked correctly: {e}")
