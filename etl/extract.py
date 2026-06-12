import pandas as  pd

DATA_PATH="data/raw"

customers=pd.read_csv(f"{DATA_PATH}/olist_customers_dataset.csv")
orders=pd.read_csv(f"{DATA_PATH}/olist_orders_dataset.csv")
products=pd.read_csv(f"{DATA_PATH}/olist_products_dataset.csv")
reviews=pd.read_csv(f"{DATA_PATH}/olist_order_reviews_dataset.csv")
payments=pd.read_csv(f"{DATA_PATH}/olist_order_payments_dataset.csv")
sellers=pd.read_csv(f"{DATA_PATH}/olist_sellers_dataset.csv")
order_items=pd.read_csv(f"{DATA_PATH}/olist_order_items_dataset.csv")
geolocation=pd.read_csv(f"{DATA_PATH}/olist_geolocation_dataset.csv")

print("customers :",customers.shape)
print("orders :",orders.shape)
print("products :",products.shape)
print("reviews :",reviews.shape)
print("payments :",payments.shape)
print("sellers :",sellers.shape)
print("order_items :",order_items.shape)
print("geolocation :",geolocation.shape)