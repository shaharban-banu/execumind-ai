from etl.extract import *
from etl.transform import *
from etl.load import *
from utils.logger import logger

customers=transform_customers(extract_customers())
load_customers(customers)

orders=transform_orders(extract_orders())
load_orders(orders)

products=transform_products(extract_products())
load_products(products)

reviews=transform_reviews(extract_reviews())
load_reviews(reviews)

sellers=transform_sellers(extract_sellers())
load_sellers(sellers)

payments=transform_payments(extract_payments())
load_payments(payments)

order_items=transform_order_items(extract_order_items())
load_order_items(order_items)

geolocation=transform_geolocation(extract_geolocation())
load_geolocation(geolocation)

logger.info("ETL pipeline completed successfully")