"""
Payment Analysis MCP Tool.

Provides business capabilities related to payment
methods, payment values, and installment usage.

The Data Intelligence Agent uses these functions
instead of generating SQL directly.
"""

from typing import Any

from mcp.tools.query_db import query_db
from utils.logger import logger


def payment_summary(mode: str = "historical"):
    """
    Retrieve overall payment statistics.

    Returns:
        - total_payments
        - total_revenue
        - average_payment
    """
    sql = """
    SELECT
        COUNT(*) AS total_payments,
        ROUND(SUM(payment_value), 2) AS total_revenue,
        ROUND(AVG(payment_value), 2) AS average_payment
    FROM payments;
    """

    logger.info("Executing payment summary")

    return query_db(sql, mode)


def payment_methods(mode: str = "historical"):
    """
    Retrieve payment method distribution.
    """
    sql = """
    SELECT
        payment_method,
        COUNT(*) AS total_transactions,
        ROUND(SUM(payment_value), 2) AS revenue
    FROM payments
    GROUP BY payment_method
    ORDER BY revenue DESC;
    """

    logger.info("Executing payment methods")

    return query_db(sql, mode)


def installment_analysis(mode: str = "historical"):
    """
    Retrieve installment usage statistics.
    """
    sql = """
    SELECT
        payment_installments,
        COUNT(*) AS transactions,
        ROUND(AVG(payment_value), 2) AS average_payment,
        ROUND(SUM(payment_value), 2) AS total_value
    FROM payments
    GROUP BY payment_installments
    ORDER BY payment_installments;
    """

    logger.info("Executing installment analysis")

    return query_db(sql, mode)


def payment_value_distribution(mode: str = "historical") :
    """
    Retrieve payment value statistics.
    """
    sql = """
    SELECT
        ROUND(MIN(payment_value), 2) AS minimum_payment,
        ROUND(MAX(payment_value), 2) AS maximum_payment,
        ROUND(AVG(payment_value), 2) AS average_payment
    FROM payments;
    """

    logger.info("Executing payment value distribution")

    return query_db(sql, mode)


def top_payment_transactions(limit: int = 10,mode: str = "historical"):
    """
    Retrieve the highest-value payment transactions.
    """
    limit = max(1, min(limit, 100))

    sql = f"""
    SELECT
        order_id,
        payment_method,
        payment_value
    FROM payments
    ORDER BY payment_value DESC
    LIMIT {limit};
    """

    logger.info("Executing top payment transactions")

    return query_db(sql, mode)