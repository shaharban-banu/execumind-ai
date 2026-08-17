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


def customer_summary(user_id:int,mode: str = "historical") :
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
        COUNT(c.customer_id) AS total_customer_records,
        COUNT(DISTINCT c.customer_master_id) AS unique_customers,
        COUNT(o.order_id) AS total_orders,
        ROUND(
            (
                COUNT(o.order_id)::numeric /
                NULLIF(COUNT(DISTINCT c.customer_master_id), 0)
            ),
            2
        ) AS average_orders_per_customer
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        WHERE c.user_id = :user_id;
    """

    logger.info("Executing customer summary")

    return query_db(sql,{"user_id": user_id}, mode)


def customer_growth(user_id:int,mode: str = "historical") :
    """
    Retrieve monthly customer acquisition.
    """

    sql = """
    SELECT
        to_char(order_date, 'YYYY-MM') AS month,
        COUNT(DISTINCT c.customer_master_id) AS new_customers
    FROM orders o JOIN customers c
    ON o.customer_id = c.customer_id
    WHERE c.user_id = :user_id
    GROUP BY month
    ORDER BY month;
    """

    logger.info("Executing customer growth")

    return query_db(sql,{"user_id": user_id}, mode)


def repeat_customer_rate(user_id:int,mode: str = "historical") :
    """
    Retrieve customers with more than one order.
    """

    sql = """
        SELECT
        ROUND(
            (
                100.0 * COUNT(*) /
                (SELECT COUNT(DISTINCT customer_master_id) FROM customers WHERE user_id = :user_id)
            )::numeric,
            2
        ) AS repeat_customer_rate
    FROM (
        SELECT c.customer_master_id
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.user_id = :user_id
        GROUP BY c.customer_master_id
        HAVING COUNT(*) > 1
        
    );
    """

    logger.info("Executing repeat customer analysis")

    return query_db(sql, {"user_id": user_id},mode)


def customers_by_state(user_id:int,mode: str = "historical"):
    """
    Retrieve customer distribution by state.
    """

    sql = """
    SELECT
        customer_state,
        COUNT(*) AS total_customers
    FROM customers
    WHERE user_id = :user_id
    GROUP BY customer_state
    ORDER BY total_customers DESC;
    """

    logger.info("Executing customers by state")

    return query_db(sql,{"user_id": user_id}, mode)


def customer_order_frequency(user_id:int,mode: str = "historical") :
    """
    Retrieve order frequency per customer.
    """

    sql = """
            SELECT
        total_orders,
        COUNT(*) AS customers
        FROM
        (
        SELECT
        customer_id,
        COUNT(*) AS total_orders
        FROM orders
        WHERE user_id = :user_id
        GROUP BY customer_id
        ) order_counts
        GROUP BY total_orders
        ORDER BY total_orders;
    """

    logger.info("Executing customer order frequency")

    return query_db(sql, {"user_id": user_id},mode)

def customer_retention(user_id:int,mode: str = "historical") :
    """
    Retrieve customer retention.
    """

    sql = """
        SELECT
        ROUND(
            (
                100.0 * COUNT(*) /
                (SELECT COUNT(DISTINCT customer_master_id) FROM customers WHERE user_id = :user_id)
            )::numeric,
            2
        ) AS customer_retention_rate
    FROM
    (
        SELECT
            c.customer_master_id
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.user_id = :user_id
        GROUP BY c.customer_master_id
        HAVING COUNT(*) > 1
    ) retained_customers;
    """

    logger.info("Executing customer retention")

    return query_db(sql, {"user_id": user_id},mode)