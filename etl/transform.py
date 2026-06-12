import pandas as pd

def transform_customers(df):
    df=df.drop_duplicates()
    df["customer_city"] = (df["customer_city"].astype(str).str.strip().str.lower())
    return df

def transform_orders(df):
    df=df.drop_duplicates()
    date_cols=[
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        df[col]=pd.to_datetime(df[col],errors='coerce')
    return df

def transform_products(df):
    df=df.drop_duplicates()
    df["product_category_name"] = (df["product_category_name"].fillna("Unknown"))

    print(df.isnull().sum())
    numeric_cols = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    return df

def transform_reviews(df):
    df=df.drop_duplicates()
    df["review_comment_title"]=(df["review_comment_title"].fillna(""))
    df["review_comment_message"] =(df["review_comment_message"] .fillna(""))
    return df

def transform_sellers(df):
    return df.drop_duplicates()

def transform_payments(df):
    return df.drop_duplicates()

def transform_order_items(df):

    df = df.drop_duplicates()

    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"],errors="coerce")
    return df

def transform_geolocation(df):
    return df.drop_duplicates()

if __name__ == "__main__":

    from etl.extract import (
        extract_customers,
        extract_orders,
        extract_products,
        extract_reviews
    )

    customers = transform_customers(
        extract_customers()
    )

    print("\nCustomers")
    print(customers.shape)
    print(customers.isnull().sum())

    orders = transform_orders(
        extract_orders()
    )

    print("\nOrders")
    print(orders.shape)
    print(orders.isnull().sum())

    products = transform_products(
        extract_products()
    )

    print("\nProducts")
    print(products.shape)
    print(products.isnull().sum())

    reviews = transform_reviews(
        extract_reviews()
    )

    print("\nReviews")
    print(reviews.shape)
    print(reviews.isnull().sum())