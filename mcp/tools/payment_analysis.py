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


def payment_summary(user_id:int,mode: str = "historical"):
    """
    Retrieve overall payment statistics.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing the total number of payments,
        total revenue, and average payment value.

    Raises:
        RuntimeError: If the database query fails.
    """
    sql = """
    SELECT
        COUNT(*) AS total_payments,
        ROUND(SUM(payment_value)::numeric, 2) AS total_revenue,
        ROUND(AVG(payment_value)::numeric, 2) AS average_payment
    FROM payments
    WHERE user_id = :user_id;
    """

    logger.info("Executing payment summary")

    try:

        return query_db(sql, {"user_id": user_id},mode)
    except Exception as exc:
        logger.exception(
            "Payment summary query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve payment summary."
        ) from exc


def payment_methods(user_id:int,mode: str = "historical"):
    """
    Retrieve payment method distribution.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing payment methods,
        transaction counts, and revenue.

    Raises:
        RuntimeError: If the database query fails.
    """
    sql = """
    SELECT
        payment_method,
        COUNT(*) AS total_transactions,
        ROUND(SUM(payment_value)::numeric, 2) AS revenue
    FROM payments
    WHERE user_id = :user_id
    GROUP BY payment_method
    ORDER BY revenue DESC;
    """

    logger.info("Executing payment methods")

    try:
        return query_db(sql,{"user_id": user_id},  mode)
    except Exception as exc:
        logger.exception(
            "Payment methods query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve payment methods."
        ) from exc


def installment_analysis(user_id:int,mode: str = "historical"):
    """
    Retrieve installment usage statistics.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing installment counts,
        average payment values, and total payment values.

    Raises:
        RuntimeError: If the database query fails.
    """
    sql = """
    SELECT
        payment_installments,
        COUNT(*) AS transactions,
        ROUND(AVG(payment_value)::numeric, 2) AS average_payment,
        ROUND(SUM(payment_value)::numeric, 2) AS total_value
    FROM payments
    WHERE user_id = :user_id
    GROUP BY payment_installments
    ORDER BY payment_installments;
    """

    logger.info("Executing installment analysis")

    try:
        return query_db(sql, {"user_id": user_id},mode)
    except Exception as exc:
        logger.exception(
            "Installment analysis query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve installment analysis."
        ) from exc


def payment_value_distribution(user_id:int,mode: str = "historical") :
    """
    Retrieve payment value statistics.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing minimum, maximum,
        and average payment values.

    Raises:
        RuntimeError: If the database query fails.
    """
    sql = """
    SELECT
        ROUND(MIN(payment_value)::numeric, 2) AS minimum_payment,
        ROUND(MAX(payment_value)::numeric, 2) AS maximum_payment,
        ROUND(AVG(payment_value)::numeric, 2) AS average_payment
    FROM payments
    WHERE user_id = :user_id;
    """

    logger.info("Executing payment value distribution")

    try:
        return query_db(sql, mode)
    except Exception as exc:
        logger.exception(
            "payment value distribution query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve payment value distribution."
        ) from exc


def top_payment_transactions(user_id:int,limit: int = 10,mode: str = "historical"):
    """
    Retrieve the highest-value payment transactions.

    Args:
        limit: Maximum number of transactions to return.
        mode: Query execution mode.

    Returns:
        Query result containing the highest-value payments.

    Raises:
        RuntimeError: If the database query fails.
    """
    limit = max(1, min(limit, 100))

    sql = f"""
    SELECT
        order_id,
        payment_method,
        payment_value
    FROM payments
    WHERE user_id = :user_id
    ORDER BY payment_value DESC
    LIMIT {limit};
    """

    logger.info("Executing top payment transactions")

    try:
        return query_db(sql, {"user_id": user_id}, mode)
    except Exception as exc:
        logger.exception(
            "Top payment transactions query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve top payment transactions."
        ) from exc