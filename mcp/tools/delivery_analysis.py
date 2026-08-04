"""
Delivery Analysis MCP Tool.

Provides business capabilities related to delivery
performance, shipping delays, and logistics.

The Data Intelligence Agent uses these functions
instead of generating SQL directly.
"""
from typing import Any
from mcp.tools.query_db import query_db
from utils.logger import logger

def delivery_summary(mode:str="historical"):
    """
    Retrieve an overall summary of delivery performance.

    Calculates the total number of orders, delivered orders,
    average delivery time, and number of late deliveries.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing delivery summary metrics.

    Raises:
        RuntimeError: If the database query fails.
    """

    sql="""select count(*) as total_orders,
        sum(
            case 
                when order_status='delivered' then 1 else 0
            end) as delivered_orders,
        ROUND(
            AVG(
                EXTRACT(EPOCH FROM (delivered_date - order_date)) / 86400
            )::numeric,
            2
        ) AS average_delivery_days,
        sum(
            case
                when delivered_date >
                estimated_delivery_date 
                then 1 else 0
            end) as late_deliveries
        from orders
        where delivered_date is not null;"""
    logger.info("Executing delivery summary")
    try:
        return query_db(sql,mode)
    except Exception as exc:
        logger.exception(
            "Delivery summary query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve delivery summary."
        ) from exc

def late_delivery_rate(mode:str="historical"):
    """
    Retrieve the percentage of late deliveries.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing the late delivery rate.

    Raises:
        RuntimeError: If the database query fails.
    """

    sql="""select 
    ROUND(
        (
            100.0 *
            SUM(
                CASE
                    WHEN delivered_date > estimated_delivery_date
                    THEN 1 ELSE 0
                END
            ) / COUNT(*)
        )::numeric,
        2
    ) AS late_delivery_rate
    from orders 
    where delivered_date is not null;"""

    logger.info("Executing late delivery rate")
    try:
        return query_db(sql,mode)
    except Exception as exc:
        logger.exception(
            "late delivery rate query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve late delivery rate."
        ) from exc

def delivery_by_state(mode:str="historical"):
    """
    Retrieve delivery performance grouped by customer state.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing delivery metrics for each state.

    Raises:
        RuntimeError: If the database query fails.
    """

    sql="""select c.customer_state,
        count(*) as total_orders,
        ROUND(
            AVG(
                EXTRACT(EPOCH FROM (delivered_date - order_date)) / 86400
            )::numeric,
            2
        ) AS average_delivery_days,
        sum(
            case
                when delivered_date >
                estimated_delivery_date 
                then 1 else 0
            end) as late_deliveries
        from orders o join customers c 
        on o.customer_id=c.customer_id
        where o.delivered_date is not null
        group by customer_state
        order by late_deliveries desc;
        """
    logger.info("Executing delivery by state ")
    try:
        return query_db(sql,mode)
    except Exception as exc:
        logger.exception(
            "Delivery by state query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve delivery by state."
        ) from exc

def delayed_orders(limit: int = 20,mode: str = "historical") :
    """
    Retrieve the most delayed customer orders.

    Args:
        limit: Maximum number of delayed orders to return.
        mode: Query execution mode.

    Returns:
        Query result containing the most delayed orders.

    Raises:
        RuntimeError: If the database query fails.
    """

    limit = max(1, min(limit, 100))

    sql = f"""
    SELECT

        order_id,

        order_date,

        estimated_delivery_date,

        delivered_date,

        ROUND(
            (
                EXTRACT(
                    EPOCH FROM (
                        delivered_date - estimated_delivery_date
                    )
                ) / 86400
            )::numeric,
            2
        ) AS delay_days

    FROM orders

    WHERE
        delivered_date >
        estimated_delivery_date

    ORDER BY delay_days DESC

    LIMIT {limit};
    """

    logger.info("Executing delayed orders")

    try:
        return query_db(sql, mode)
    except Exception as exc:
        logger.exception(
            "Delayed orders query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve delayed orders."
        ) from exc


def order_status_distribution(mode: str = "historical"):
    """
    Retrieve the distribution of customer order statuses.

    Args:
        mode: Query execution mode.

    Returns:
        Query result containing the number of orders in each
        status category.

    Raises:
        RuntimeError: If the database query fails.
    """

    sql = """
    SELECT
        order_status,
        COUNT(*) AS total_orders
    FROM orders
    GROUP BY order_status
    ORDER BY total_orders DESC;
    """

    logger.info("Executing order status distribution")

    try:
        return query_db(sql, mode)
    except Exception as exc:
        logger.exception(
            "order status distribution query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve order status distribution."
        ) from exc
