from database.database import engine

def load_customers(df):
    df.to_sql("customers",engine,if_exists="replace",index=False)
    print("customer loaded.")

def load_orders(df):
    df.to_sql("orders",engine,if_exists="replace",index=False)
    print("orders loaded.")

def load_products(df):
    df.to_sql("products",engine,if_exists="replace",index=False)
    print("products loaded.")

def load_reviews(df):
    df.to_sql("reviews",engine,if_exists="replace",index=False)
    print("reviews loaded.")

def load_sellers(df):
    df.to_sql("sellers",engine,if_exists="replace",index=False)
    print("sellers loaded.")

def load_payments(df):
    df.to_sql("payments",engine,if_exists="replace",index=False)
    print("payments loaded.")

def load_order_items(df):
    df.to_sql("order_items",engine,if_exists="replace",index=False)
    print("order_items loaded.")

def load_geolocation(df):
    df.to_sql("geolocation",engine,if_exists="replace",index=False)
    print("geolocation loaded.")