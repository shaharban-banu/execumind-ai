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


def product_summary(mode: str = "historical"):
    """
    Retrieve overall product statistics.
    """
    sql = """
    SELECT
        COUNT(DISTINCT product_id) AS total_products,
        COUNT(DISTINCT category) AS total_categories,
        ROUND(AVG(weight), 2) AS average_weight
    FROM products;
    """

    logger.info("Executing product summary")

    return query_db(sql, mode)


def category_performance(mode: str = "historical"):
    """
    Retrieve revenue and sales by product category.
    """
    sql = """
    SELECT
        COALESCE(ct.category_english,p.category) AS category,
        COUNT(*) AS items_sold,
        ROUND(SUM(oi.item_price), 2) AS revenue

    FROM order_items oi

    JOIN products p
        ON oi.product_id = p.product_id

    LEFT JOIN category_translation ct
        ON p.category = ct.category

    GROUP BY COALESCE(ct.category_english,p.category)

    ORDER BY revenue DESC;
    """

    logger.info("Executing category performance")

    return query_db(sql, mode)


def top_products(limit: int = 10,mode: str = "historical") :
    """
    Retrieve top-selling products by revenue.
    """
    limit = max(1, min(limit, 100))

    sql = f"""
    SELECT
        product_id,
        COUNT(*) AS units_sold,
        ROUND(SUM(item_price), 2) AS revenue

    FROM order_items

    GROUP BY product_id

    ORDER BY revenue DESC

    LIMIT {limit};
    """

    logger.info("Executing top products")

    return query_db(sql, mode)


def product_price_statistics(mode: str = "historical") :
    """
    Retrieve pricing statistics for sold products.
    """
    sql = """
    SELECT
        ROUND(MIN(item_price), 2) AS minimum_price,
        ROUND(MAX(item_price), 2) AS maximum_price,
        ROUND(AVG(item_price), 2) AS average_price
    FROM order_items;
    """

    logger.info("Executing product price statistics")

    return query_db(sql, mode)


def category_distribution(mode: str = "historical"):
    """
    Retrieve the number of products in each category.
    """
    sql = """
    SELECT
        coalesce(ct.category_english,p.category) AS category,
        COUNT(*) AS total_products

    FROM products p

    LEFT JOIN category_translation ct
        ON p.category = ct.category

    GROUP BY coalesce(ct.category_english,p.category)

    ORDER BY total_products DESC;
    """

    logger.info("Executing category distribution")

    return query_db(sql, mode)