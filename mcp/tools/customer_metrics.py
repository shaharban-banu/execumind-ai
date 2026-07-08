"""
Customer Metrics MCP Tool.

Provides business capabilities related to customer
growth, retention, and purchasing behaviour.

The Data Intelligence Agent uses these functions
instead of generating SQL directly.
"""

from typing import Any
from mcp.tools.query_db import query_db
from utils.logger import logger


def customer_summary(mode: str = "historical") :
    """
    Retrieve overall customer statistics.

    Returns:
        - total_customers
        - unique_customers
        - total_orders
        - average_orders_per_customer
    """
    sql = """
    SELECT
        COUNT(DISTINCT c.customer_id) AS total_customers,
        COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
        COUNT(o.order_id) AS total_orders,
        ROUND(
            CAST(COUNT(o.order_id) AS REAL) /
            NULLIF(COUNT(DISTINCT c.customer_unique_id),0),
            2
        ) AS average_orders_per_customer
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id;
    """

    logger.info("Executing customer summary")

    return query_db(sql, mode)


def customer_growth(mode: str = "historical") :
    """
    Retrieve monthly customer acquisition.
    """

    sql = """
    SELECT
        strftime('%Y-%m', order_date) AS month,
        COUNT(DISTINCT customer_id) AS new_customers
    FROM orders
    GROUP BY month
    ORDER BY month;
    """

    logger.info("Executing customer growth")

    return query_db(sql, mode)


def repeat_customer_rate(mode: str = "historical") :
    """
    Retrieve customers with more than one order.
    """

    sql = """
    SELECT
        customer_unique_id,
        COUNT(o.order_id) AS total_orders
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY customer_unique_id
    HAVING COUNT(o.order_id) > 1
    ORDER BY total_orders DESC;
    """

    logger.info("Executing repeat customer analysis")

    return query_db(sql, mode)


def customers_by_state(mode: str = "historical"):
    """
    Retrieve customer distribution by state.
    """

    sql = """
    SELECT
        state,
        COUNT(*) AS total_customers
    FROM customers
    GROUP BY state
    ORDER BY total_customers DESC;
    """

    logger.info("Executing customers by state")

    return query_db(sql, mode)


def customer_order_frequency(mode: str = "historical") :
    """
    Retrieve order frequency per customer.
    """

    sql = """
    SELECT
        customer_unique_id,
        COUNT(o.order_id) AS total_orders
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY customer_unique_id
    ORDER BY total_orders DESC;
    """

    logger.info("Executing customer order frequency")

    return query_db(sql, mode)