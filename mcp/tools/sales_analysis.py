"""
Sales Analysis MCP Tool.

Provides business capabilities related to sales performance.
The Data Intelligence Agent uses these functions instead of
writing SQL directly.
"""
from typing import Any
from mcp.tools.query_db import query_db
from utils.logger import logger

def sales_summary(mode:str="historical"):
    """
    Retrieve overall sales summary.

    Returns:
        List containing:
            - total_orders
            - total_revenue
            - average_order_value
    """
    sql="""SELECT
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(payment_value),2) AS total_revenue,
        ROUND(SUM(payment_value) / COUNT(DISTINCT order_id),2) AS average_order_value
    FROM payments;
    """ 
    logger.info("Executing sales summary")

    try:
        return query_db(sql,mode)
    except Exception as exc:
        logger.exception(
            "Sales summary query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve sales summary."
        ) from exc

def monthly_sales(mode:str="historical"):
    """
    Retrieve monthly revenue trend.
    """
    sql="""select 
        strftime('%Y-%m',o.order_date) as month,
        round(sum(p.payment_value),2) as revenue,
        count(distinct o.order_id) as orders
        from orders o join payments p
        on o.order_id=p.order_id
        group by month order by month;"""
    logger.info("Executing monthly sales")

    try:
        return query_db(sql,mode)
    except Exception as exc:
        logger.exception(
            "Monthly sales query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve monthly sales."
        ) from exc

def sales_by_state(mode:str="historical"):
    sql="""select
        c.customer_state,
        round(sum(p.payment_value),2) as revenue,
        count(distinct o.order_id) as total_orders
        from orders o join customers c
        on o.customer_id=c.customer_id
        join payments p on o.order_id=p.order_id
        group by c.customer_state
        order by revenue desc;
        """
    logger.info("Executing sales by state")

    try:
        return query_db(sql,mode)
    except Exception as exc:
        logger.exception(
            "Sales by state query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve sales by state."
        ) from exc

def sales_by_category(mode:str="historical"):
    sql="""SELECT
            p.product_category,
            ROUND(SUM(oi.order_item_value),2) AS revenue,
            SUM(oi.quantity) AS items_sold
        FROM order_items oi
        JOIN products p
        ON oi.product_id=p.product_id
        GROUP BY p.product_category
        ORDER BY revenue DESC;"""
    
    logger.info("Executing sales by category")

    try:
        return query_db(sql,mode)
    except Exception as exc:
        logger.exception(
            "Sales by category query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve sales by category."
        ) from exc

def top_products(limit: int = 10,mode: str = "historical") :
    """
    Retrieve top-selling products.
    """

    sql = f"""
    SELECT
        product_id,
        SUM(quantity) AS units_sold,
        ROUND(SUM(order_item_value),2) AS revenue
    FROM order_items
    GROUP BY product_id
    ORDER BY revenue DESC
    LIMIT {limit};
    """

    logger.info("Executing top products")

    try:
        return query_db(sql, mode)
    except Exception as exc:
        logger.exception(
            "Top products query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve top products."
        ) from exc
