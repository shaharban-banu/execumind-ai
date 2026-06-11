# config/dataset_config.py

DATASETS = {

    "customers": {
        "file": "olist_customers_dataset.csv",
        "primary_key": "customer_id",
        "date_columns": [],
        "text_columns": []
    },

    "orders": {
        "file": "olist_orders_dataset.csv",
        "primary_key": "order_id",
        "date_columns": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "text_columns": []
    },

    "order_items": {
        "file": "olist_order_items_dataset.csv",
        "primary_key":  ["order_id","order_item_id"],
        "date_columns": [
            "shipping_limit_date"
        ],
        "text_columns": []
    },

    "payments": {
        "file": "olist_order_payments_dataset.csv",
        "primary_key": ["order_id","payment_sequential"],
        "date_columns": [],
        "text_columns": []
    },

    "products": {
        "file": "olist_products_dataset.csv",
        "primary_key": "product_id",
        "date_columns": [],
        "text_columns": []
    },

    "sellers": {
        "file": "olist_sellers_dataset.csv",
        "primary_key": "seller_id",
        "date_columns": [],
        "text_columns": []
    },

    "reviews": {
        "file": "olist_order_reviews_dataset.csv",
        "primary_key": None,
        "date_columns": [
            "review_creation_date",
            "review_answer_timestamp"
        ],
        "text_columns": [
            "review_comment_message"
        ]
    },

    "geolocation": {
        "file": "olist_geolocation_dataset.csv",
        "primary_key": None,
        "date_columns": [],
        "text_columns": []
    }
}
# DATASETS={
#     "customers":"olist_customers_dataset.csv",
#     "orders": "olist_orders_dataset.csv",
#     "order_items": "olist_order_items_dataset.csv",
#     "payments": "olist_order_payments_dataset.csv",
#     "products": "olist_products_dataset.csv",
#     "reviews": "olist_order_reviews_dataset.csv",
#     "sellers": "olist_sellers_dataset.csv",
#     "geolocation": "olist_geolocation_dataset.csv"

# }