"""
entities.py

Defines the canonical business entities supported by the
AI-powered ingestion engine.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BusinessEntity:
    """
    Represents a canonical business entity.
    """

    name: str

    description: str

    aliases: list[str] = field(default_factory=list)


CUSTOMERS = BusinessEntity(
    name="customers",
    description="Represents people or organizations purchasing products.",
    aliases=[
        "customer",
        "customers",
        "client",
        "clients",
        "buyer",
        "buyers",
        "consumer",
        "consumers",
        "user",
        "users",
    ],
)

ORDERS = BusinessEntity(
    name="orders",
    description="Represents purchase transactions.",
    aliases=[
        "order",
        "orders",
        "sale",
        "sales",
        "purchase",
        "purchases",
        "transaction",
        "transactions",
    ],
)

PRODUCTS = BusinessEntity(
    name="products",
    description="Represents items available for sale.",
    aliases=[
        "product",
        "products",
        "item",
        "items",
        "goods",
        "catalog",
        "inventory",
    ],
)

PAYMENTS = BusinessEntity(
    name="payments",
    description="Represents payment information.",
    aliases=[
        "payment",
        "payments",
        "invoice",
        "billing",
        "receipt",
    ],
)

SELLERS = BusinessEntity(
    name="sellers",
    description="Represents merchants or vendors.",
    aliases=[
        "seller",
        "sellers",
        "vendor",
        "vendors",
        "merchant",
        "merchants",
        "supplier",
        "suppliers",
    ],
)

REVIEWS = BusinessEntity(
    name="reviews",
    description="Represents customer feedback.",
    aliases=[
        "review",
        "reviews",
        "rating",
        "ratings",
        "feedback",
        "comments",
        "order review",
        "order reviews",
        "customer review",
        "customer reviews",
    ],
)

DELIVERY = BusinessEntity(
    name="deliveries",
    description="Represents shipment and delivery information.",
    aliases=[
        "delivery",
        "deliveries",
        "shipment",
        "shipments",
        "shipping",
        "dispatch",
        "fulfillment",
        "logistics",
    ],
)

ORDER_ITEMS=BusinessEntity(
    name="order_items",
    description="Represents individual items within an order.",
    aliases=[ "order_item",
        "order_items",
        "order line",
        "order lines",
        "line item",
        "line items",
        "order detail",
        "order details",
        "sales detail",
        "sales details",
        "purchase item",
        "purchase items",
        "cart item",
        "cart items",
        "invoice item",
        "invoice items",
        "transaction item",
        "transaction items",
        ],
)


BUSINESS_ENTITIES = [
    CUSTOMERS,
    ORDERS,
    PRODUCTS,
    PAYMENTS,
    SELLERS,
    REVIEWS,
    DELIVERY,
    ORDER_ITEMS,
]