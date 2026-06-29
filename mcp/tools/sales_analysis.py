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
    sql="""select count(distinct o.order_id) as total_order,
    round(sum(p.payment_value),2) as total_revenue,
    round(avg(p.payment_value),2) as average_order_value
    from orders o join payments p
    on o.order_id=p.order_id;
    """ 
    logger.info("Executing sales summary")
    return query_db(sql,mode)

def monthly_sales(mode:str="historical"):
    """
    Retrieve monthly revenue trend.
    """
    sql="""select 
        strftime('%Y-%m',order_purchase_timestamp) as month,
        round(sum(p.payment_value),2) as revenue,
        count(distinct o.order_id) as orders
        from orders o join payments p
        on o.order_id=p.order_id
        group by month order by month;"""
    logger.info("Executing monthly sales")
    return query_db(sql,mode)

def sales_by_state(mode:str="historical"):
    sql="""select
        c.customer_state
        round(sum(p.payment_value),2) as revenue,
        count(distinct o.order_id) as total_orders
        from orders o join customers c
        on o.customer_id=c.customer_id
        join payments p on o.order_id=p.order_id
        group by c.customer_state
        order by revenue desc;
        """
    logger.info("Executing sales by state")
    return query_db(sql,mode)

def sales_by_category(mode:str="historical"):
    sql="""select 
    ct.product_category_name_english as category,
    round(sum(oi.price),2) as revenue,
    count(*) as items_sold
    from order_items oi join products pr 
        on oi.product_id=pr.product_id 
    join category_translation ct 
        on pr.product_category_name=ct.product_category_name
        group by category order by revenue desc; """
    
    logger.info("Executing sales by category")
    return query_db(sql,mode)

def top_products(limit: int = 10,mode: str = "historical") :
    """
    Retrieve top-selling products.
    """

    sql = f"""
    SELECT
        product_id,
        COUNT(*) AS units_sold,
        ROUND(SUM(price), 2) AS revenue
    FROM order_items
    GROUP BY product_id
    ORDER BY revenue DESC
    LIMIT {limit};
    """

    logger.info("Executing top products")

    return query_db(sql, mode)
