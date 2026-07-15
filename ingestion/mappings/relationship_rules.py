"""
relationship_rules.py

Defines valid business relationships between canonical entities.
"""

RELATIONSHIP_RULES = {
    "orders": {
        "customers": "customer_id",
    },

    "payments": {
        "orders": "order_id",
    },

    "reviews": {
        "orders": "order_id",
    },

    "delivery": {
        "orders": "order_id",
    },

    "products": {
        "sellers": "seller_id",
    },
    "order_items": {
        "orders": "order_id",
        "products": "product_id",
        "sellers": "seller_id",
    },
}