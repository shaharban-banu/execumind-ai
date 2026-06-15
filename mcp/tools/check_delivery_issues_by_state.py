"""
Delivery Issues By State Analysis Tool.

Analyzes delivery delays by customer state
and identifies regions with the highest
delivery delay rates.
"""
from utils.logger import logger
import pandas as pd

from database.database import engine
from sqlalchemy import text

def check_delivery_issues_by_state(top_n:int=10):
    """
    Analyze delivery delays by customer state.

    Args:
        top_n:
            Number of states to return.

    Returns:
        list[dict]:
            State-level delivery metrics.
    """
    try:
        query="""select c.customer_state,
        o.order_estimated_delivery_date,
        o.order_delivered_customer_date
        from orders o join customers c
        on o.customer_id=c.customer_id
        where o.order_status='delivered'
        and order_delivered_customer_date is not null
        and order_estimated_delivery_date is not null"""

        df=pd.read_sql(text(query),engine)
        logger.info("Loaded %s delivered orders",len(df))

        df['order_estimated_delivery_date']=pd.to_datetime(df['order_estimated_delivery_date'])
        df['order_delivered_customer_date']=pd.to_datetime(df['order_delivered_customer_date'])

        df['delay_days']=(df['order_delivered_customer_date']-df['order_estimated_delivery_date']).dt.days

        grouped =(df.groupby("customer_state").agg(
            total_orders=("customer_state","count"),
            late_orders=("delay_days",lambda x:(x>0).sum()),
            avg_delay_days=("delay_days",lambda x:round((x>0).mean(),2)if (x>0).any() else 0)

        ).reset_index())

        grouped["delay_rate_percent"]=round((grouped['late_orders']/grouped['total_orders'])*100,2)
        grouped=grouped.sort_values(by="delay_rate_percent",ascending=False)
        results=(grouped.head(top_n).to_dict(orient="records"))

        logger.info("Generated delay analysis"
                    "for %s states",len(results))
        return results
    except Exception:
        logger.exception("State delivery analysis failed")
        raise

if __name__=="__main__":
    results=(check_delivery_issues_by_state())
    print("\nDelivery issues by State")
    print("="*50)

    for row in results:
        print(f"\nState : {row['customer_state']}")
        print(f"Total orders : {row['total_orders']}")
        print(f"Late Orders : {row['late_orders']}")
        print(f"delay Rate : {row['delay_rate_percent']}%")
        print(f"Avg Delay Days : {row['avg_delay_days']}")


