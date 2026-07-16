"""
field_types.py

Defines the canonical fields for each supported business entity.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CanonicalField:
    """
    Represents a canonical business field.
    """

    name: str
    entity: str
    data_type: str

    required: bool = False
    identifier: bool = False
    description: str = ""


# ============================================================
# CUSTOMER
# ============================================================

CUSTOMER_FIELDS = [
    CanonicalField(
        name="customer_id",
        entity="customers",
        data_type="string",
        required=True,
        identifier=True,
        description="Unique customer identifier.",
    ),
    CanonicalField(
        name="customer_master_id",
        entity="customers",
        data_type="string",
        required=False,
    ),
    CanonicalField(
        name="customer_name",
        entity="customers",
        data_type="string",
        description="Customer full name.",
    ),
    CanonicalField(
        name="customer_email",
        entity="customers",
        data_type="string",
        description="Customer email address.",
    ),
    CanonicalField(
        name="customer_phone",
        entity="customers",
        data_type="string",
        description="Customer phone number.",
    ),
    CanonicalField(
        name="customer_city",
        entity="customers",
        data_type="string",
        description="Customer city.",
    ),
    CanonicalField(
        name="customer_state",
        entity="customers",
        data_type="string",
        description="Customer state.",
    ),
    CanonicalField(
        name="customer_country",
        entity="customers",
        data_type="string",
        description="Customer country.",
    ),
    CanonicalField(
        name="customer_created_date",
        entity="customers",
        data_type="datetime",
        description="Customer registration date.",
    ),
]

# ============================================================
# ORDERS
# ============================================================

ORDER_FIELDS = [
    CanonicalField(
        name="order_id",
        entity="orders",
        data_type="string",
        required=True,
        identifier=True,
        description="Unique order identifier.",
    ),
    CanonicalField(
        name="customer_id",
        entity="orders",
        data_type="string",
        required=True,
        description="Customer placing the order.",
    ),
    CanonicalField(
        name="order_date",
        entity="orders",
        data_type="datetime",
        description="Order creation date.",
    ),
    CanonicalField(
        name="order_status",
        entity="orders",
        data_type="string",
        description="Current order status.",
    ),
    CanonicalField(
        name="order_value",
        entity="orders",
        data_type="float",
        description="Total order value.",
    ),
    CanonicalField(
        name="estimated_delivery_date",
        entity="orders",
        data_type="datetime",
        description="Estimated delivery date.",
    ),
    CanonicalField(
        name="delivered_date",
        entity="orders",
        data_type="datetime",
        description="Actual delivery date.",
    ),
]

# ============================================================
# PRODUCTS
# ============================================================

PRODUCT_FIELDS = [
    CanonicalField(
        name="product_id",
        entity="products",
        data_type="string",
        required=True,
        identifier=True,
        description="Unique product identifier.",
    ),
    CanonicalField(
        name="product_name",
        entity="products",
        data_type="string",
        description="Product name.",
    ),
    CanonicalField(
        name="product_category",
        entity="products",
        data_type="string",
        description="Product category.",
    ),
    CanonicalField(
        name="price",
        entity="products",
        data_type="float",
        description="Product price.",
    ),
    CanonicalField(
        name="weight",
        entity="products",
        data_type="float",
        description="Product weight.",
    ),
]

# ============================================================
# PAYMENTS
# ============================================================

PAYMENT_FIELDS = [
    CanonicalField(
        name="payment_id",
        entity="payments",
        data_type="string",
        required=True,
        identifier=True,
        description="Unique payment identifier.",
    ),
    CanonicalField(
        name="order_id",
        entity="payments",
        data_type="string",
        required=True,
        description="Associated order identifier.",
    ),
    CanonicalField(
        name="payment_method",
        entity="payments",
        data_type="string",
        description="Payment method.",
    ),
    CanonicalField(
        name="payment_value",
        entity="payments",
        data_type="float",
        description="Payment amount.",
    ),
    CanonicalField(
        name="payment_installments",
        entity="payments",
        data_type="integer",
        description="Number of payment installments.",
    ),
]

# ============================================================
# SELLERS
# ============================================================

SELLER_FIELDS = [
    CanonicalField(
        name="seller_id",
        entity="sellers",
        data_type="string",
        required=True,
        identifier=True,
        description="Unique seller identifier.",
    ),
    CanonicalField(
        name="seller_name",
        entity="sellers",
        data_type="string",
        description="Seller name.",
    ),
    CanonicalField(
        name="seller_city",
        entity="sellers",
        data_type="string",
        description="Seller city.",
    ),
    CanonicalField(
        name="seller_state",
        entity="sellers",
        data_type="string",
        description="Seller state.",
    ),
]

# ============================================================
# REVIEWS
# ============================================================

REVIEW_FIELDS = [
    CanonicalField(
        name="review_id",
        entity="reviews",
        data_type="string",
        required=True,
        identifier=True,
        description="Unique review identifier.",
    ),
    CanonicalField(
        name="order_id",
        entity="reviews",
        data_type="string",
        required=True,
        description="Associated order identifier.",
    ),
    CanonicalField(
        name="review_score",
        entity="reviews",
        data_type="integer",
        description="Review rating score.",
    ),
    CanonicalField(
        name="review_title",
        entity="reviews",
        data_type="string",
        description="Review title.",
    ),
    CanonicalField(
        name="review_comment",
        entity="reviews",
        data_type="string",
        description="Review comment.",
    ),
    CanonicalField(name="review_text",entity="reviews", data_type="string"),
    CanonicalField(
        name="review_date",
        entity="reviews",
        data_type="datetime",
        description="Review creation date.",
    ),
]

# ============================================================
# DELIVERY
# ============================================================

DELIVERY_FIELDS = [
    CanonicalField(
        name="delivery_id",
        entity="deliveries",
        data_type="string",
        required=True,
        identifier=True,
        description="Unique delivery identifier.",
    ),
    CanonicalField(
        name="order_id",
        entity="delivery",
        data_type="string",
        required=True,
        description="Associated order identifier.",
    ),
    CanonicalField(
        name="carrier",
        entity="delivery",
        data_type="string",
        description="Shipping carrier.",
    ),
    CanonicalField(
        name="shipped_date",
        entity="delivery",
        data_type="datetime",
        description="Shipment date.",
    ),
    CanonicalField(
        name="delivered_date",
        entity="delivery",
        data_type="datetime",
        description="Delivery date.",
    ),
    CanonicalField(
        name="delivery_status",
        entity="delivery",
        data_type="string",
        description="Delivery status.",
    ),
    CanonicalField(
        name="freight_cost",
        entity="delivery",
        data_type="float",
        description="Shipping cost.",
    ),
]

ORDER_ITEM_FIELDS = [
    CanonicalField(
        name="order_item_id",
        entity="order_items",
        data_type="string",
        required=True,
        identifier=True,
    ),
    CanonicalField(
        name="order_id",
        entity="order_items",
        data_type="string",
        required=True,
    ),
    CanonicalField(
        name="product_id",
        entity="order_items",
        data_type="string",
        required=True,
    ),
    CanonicalField(
        name="seller_id",
        entity="order_items",
        data_type="string",
    ),
    CanonicalField(
        name="quantity",
        entity="order_items",
        data_type="integer",
    ),
    CanonicalField(
        name="unit_price",
        entity="order_items",
        data_type="float",
    ),
    CanonicalField(
    name="freight_cost",
    entity="order_items",
    data_type="float",
    ),
    CanonicalField(
    name="order_item_value",
    entity="order_items",
    data_type="float",
    ),
]
# ============================================================
# LOOKUP DICTIONARY
# ============================================================

ENTITY_FIELDS = {
    "customers": CUSTOMER_FIELDS,
    "orders": ORDER_FIELDS,
    "products": PRODUCT_FIELDS,
    "payments": PAYMENT_FIELDS,
    "sellers": SELLER_FIELDS,
    "reviews": REVIEW_FIELDS,
    "deliveries": DELIVERY_FIELDS,
    "order_items":ORDER_ITEM_FIELDS,
}