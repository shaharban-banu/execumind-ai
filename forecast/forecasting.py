"""
Forecast Data Loader.

Provides historical time series used for
forecast model training.
"""
import pandas as pd
from database.database import engine

FORECAST_QUERIES={
    "revenue":"""select 
                strftime('%Y-%m',o.order_date) as ds,
                sum(p.sales_amount) as y
            from orders o join payments p
            on o.order_id=p.order_id
            group by ds
            order by ds;
        """,
    "orders":"""
        select
            strftime('%Y-%m',order_date) as ds,
            count(*) as y
            from orders group by ds order by ds;
        """,
    "customers":"""
        select
            strftime('%Y-%m',order_date) as ds,
            count(distinct customer_id) as y 
            from orders group by ds order by ds;
        """,
    "aov":"""
        select 
            strftime('%Y-%m',o.order_date) as ds,
            avg(p.sales_amount) as y
            from orders o join payments p
            on o.order_id=p.order_id
            group by ds order by ds""",
} 

def load_time_series(metric):
    """load historical time series"""
    if metric not in FORECAST_QUERIES:
        raise ValueError(f"unknown metric : {metric}")
    df=pd.read_sql(FORECAST_QUERIES[metric],engine)
    df['ds']=pd.to_datetime(df['ds'])

    #df=df[df['y']>10000].copy()
    return df 