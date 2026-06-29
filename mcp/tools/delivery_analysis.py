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
    sql="""select count(*) as total_orders,
        sum(
            case 
                when order_status='delivered' then 1 else 0
            end) as delivered_orders,
        round(avg(julianday(order_delivered_customer_date)-
                julianday(order_purchase_timestamp)),2)
                as average_delivery_days,
        sum(
            case
                when order_delivered_customer_date >
                order_estimated_delivery_date 
                then 1 else 0
            end) as late_deliveries
        from orders
        where order_delivered_customer_date is not null;"""
    logger.info("Executing delivery summary")
    return query_db(sql,mode)

def late_delivery_rate(mode:str="historical"):
    sql="""select 
    round(
        100.0*
        sum(
            case
                when order_delivered_customer_date>
                order_estimated_delivery_date
                then 1 else 0
            end
        ) / count(*)
    ,2) as late_delivery_rate
    from orders 
    where order_delivered_customer_date is not null;"""

    logger.info("Executing late delivery rate")
    return query_db(sql,mode)

def delivery_by_state(mode:str="historical"):
    sql="""select c.customer_state,
        count(*) as total_orders,
        round(avg(julianday(order_delivered_customer_date)-
                julianday(order_purchase_timestamp)),2)
                as average_delivery_days,
        sum(
            case
                when order_delivered_customer_date >
                order_estimated_delivery_date 
                then 1 else 0
            end) as late_deliveries
        from orders o join customer c 
        on o.customer_id=c.customer_id
        where o.order_delivered_customer_date is not null
        group by c.customer_state
        order by late_deliveries desc;
        """
    logger.info("Executing delivery by state ")
    return query_db(sql,mode)

def delayed_orders(limit: int = 20,mode: str = "historical") :
    """
    Retrieve the most delayed customer orders.
    """

    limit = max(1, min(limit, 100))

    sql = f"""
    SELECT

        order_id,

        order_purchase_timestamp,

        order_estimated_delivery_date,

        order_delivered_customer_date,

        ROUND(
            julianday(order_delivered_customer_date) -
            julianday(order_estimated_delivery_date),
            2
        ) AS delay_days

    FROM orders

    WHERE
        order_delivered_customer_date >
        order_estimated_delivery_date

    ORDER BY delay_days DESC

    LIMIT {limit};
    """

    logger.info("Executing delayed orders")

    return query_db(sql, mode)


def order_status_distribution(mode: str = "historical"):
    """
    Retrieve order status distribution.
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

    return query_db(sql, mode)
