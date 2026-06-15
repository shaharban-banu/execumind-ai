"""
Delivery Issues Analysis Tool.

Analyzes delivery performance and
returns key fulfillment metrics.
"""
import pandas as pd
from sqlalchemy import text
from database.database import engine
from utils.logger import logger

def check_delivery_issues():
    """
    Analyze delivery delays.

    Returns:
        dict[str, Any]:
            Delivery performance metrics.
    """
    try:
        query="""select 
        order_id,order_estimated_delivery_date,
        order_delivered_customer_date
        from orders
        where order_status='delivered'
        and order_delivered_customer_date is not null
        and order_estimated_delivery_date is not null"""

        df=pd.read_sql(text(query),engine)
        logger.info("Loaded %s delivered order",len(df))

        df['order_estimated_delivery_date']=pd.to_datetime(df['order_estimated_delivery_date'])
        df['order_delivered_customer_date']=pd.to_datetime(df['order_delivered_customer_date'])

        df['delay_days']=(df['order_delivered_customer_date']-df['order_estimated_delivery_date']).dt.days
       
        late_orders=df[df['delay_days']>0]
        total_delivered_orders=len(df)
        total_late_orders=len(late_orders)

        delay_rate=round((total_late_orders/total_delivered_orders)*100,2)
        avg_delay_days=round(late_orders['delay_days'].mean(),2)
        max_delay_day=int(late_orders['delay_days'].max())

        result={
            "total_delivered_orders":total_delivered_orders,
            "late_orders":total_late_orders,
            "maximum_delay_day":max_delay_day,
            "delay_rate_percent":delay_rate,
            "average_delay_days":avg_delay_days
        }

        logger.info("Delivery analysis completed")
        return result
    except Exception:
        logger.exception("Delivery issue analysis failed")
        raise

#Test
if __name__=="__main__":
    result=check_delivery_issues()
    print("\nDelivery Issues :")
    print("="*50)

    for key,value in result.items():
        print(f"{key} : {value}")