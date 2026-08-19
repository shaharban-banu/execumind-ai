"""
Product Analysis MCP Tool.

Provides business capabilities related to product
performance, categories, and pricing.

The Data Intelligence Agent uses these functions
instead of generating SQL directly.
"""

from typing import Any

from mcp.tools.query_db import query_db
from utils.logger import logger


def product_summary(user_id:int,mode: str = "historical"):
    """
    Retrieve overall product statistics.
    """
    sql = """
    SELECT
        COUNT(DISTINCT product_id) AS total_products,
        COUNT(DISTINCT product_category) AS total_categories,
        ROUND(AVG(weight)::numeric, 2) AS average_weight
    FROM products
    WHERE user_id = :user_id;
    """

    logger.info("Executing product summary")

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


def category_performance(user_id:int,mode: str = "historical"):
    """
    Retrieve revenue and sales by product category.
    """
    sql = """
    SELECT
        p.product_category,
        COUNT(*) AS items_sold,
        ROUND(SUM(oi.order_item_value)::numeric, 2) AS revenue

    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.user_id = :user_id
    GROUP BY p.product_category

    ORDER BY revenue DESC;
    """

    logger.info("Executing category performance")

    try:
        return query_db(sql, {"user_id": user_id}, mode)
    except Exception as exc:
        logger.exception(
            "Category performance query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve Category performance."
        ) from exc


def top_products(user_id:int,limit: int = 10,mode: str = "historical") :
    """
    Retrieve top-selling products by revenue.
    """
    limit = max(1, min(limit, 100))

    sql = f"""
    SELECT
        product_id,
        SUM(quantity) AS units_sold,
        ROUND(SUM(order_item_value)::numeric, 2) AS revenue

    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.user_id = :user_id

    GROUP BY product_id

    ORDER BY revenue DESC

    LIMIT {limit};
    """

    logger.info("Executing top products")

    try:
        return query_db(sql, {"user_id": user_id}, mode)
    except Exception as exc:
        logger.exception(
            "Top products query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve top products."
        ) from exc


def product_price_statistics(user_id:int,mode: str = "historical") :
    """
    Retrieve pricing statistics for sold products.
    """
    sql = """
    SELECT
        ROUND(MIN(unit_price)::numeric, 2) AS minimum_price,
        ROUND(MAX(unit_price)::numeric, 2) AS maximum_price,
        ROUND(AVG(unit_price)::numeric, 2) AS average_price
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.user_id = :user_id;
    """

    logger.info("Executing product price statistics")

    try:
        return query_db(sql, {"user_id": user_id}, mode)
    except Exception as exc:
        logger.exception(
            "product price statistics query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve product price statistics."
        ) from exc


def category_distribution(user_id:int,mode: str = "historical"):
    """
    Retrieve the number of products in each category.
    """
    sql = """
    SELECT
        product_category,
        COUNT(*) AS total_products

    FROM products p

    WHERE user_id = :user_id
    GROUP BY product_category

    ORDER BY total_products DESC;
    """

    logger.info("Executing category distribution")

    try:
        return query_db(sql, {"user_id": user_id}, mode)
    except Exception as exc:
        logger.exception(
            "category distribution query failed: %s",
            exc,
        )
        raise RuntimeError(
            "Failed to retrieve category distribution."
        ) from exc