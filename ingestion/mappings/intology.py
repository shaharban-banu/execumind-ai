"""
ontology.py

Defines business concepts and semantic relationships used by the
AI-powered ingestion engine.

Unlike synonyms, ontology groups words into business concepts.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BusinessConcept:
    """
    Represents a business concept and its related vocabulary.
    """

    canonical_name: str

    description: str

    keywords: list[str] = field(default_factory=list)


# ==========================================================
# CUSTOMER
# ==========================================================

CUSTOMER = BusinessConcept(
    canonical_name="customer",
    description="A person or organization purchasing products.",
    keywords=[
        "customer",
        "client",
        "buyer",
        "consumer",
        "shopper",
        "member",
        "account",
        "user",
    ],
)

# ==========================================================
# ORDER
# ==========================================================

ORDER = BusinessConcept(
    canonical_name="order",
    description="A purchase transaction.",
    keywords=[
        "order",
        "purchase",
        "sale",
        "transaction",
        "booking",
        "invoice",
    ],
)

# ==========================================================
# PRODUCT
# ==========================================================

PRODUCT = BusinessConcept(
    canonical_name="product",
    description="An item available for sale.",
    keywords=[
        "product",
        "item",
        "goods",
        "merchandise",
        "sku",
        "article",
    ],
)

# ==========================================================
# PAYMENT
# ==========================================================

PAYMENT = BusinessConcept(
    canonical_name="payment",
    description="Financial transaction information.",
    keywords=[
        "payment",
        "billing",
        "invoice_payment",
        "transaction_payment",
        "amount",
        "price",
        "cost",
        "fee",
        "value",
    ],
)

# ==========================================================
# DELIVERY
# ==========================================================

DELIVERY = BusinessConcept(
    canonical_name="delivery",
    description="Shipment and logistics information.",
    keywords=[
        "delivery",
        "shipment",
        "shipping",
        "dispatch",
        "courier",
        "carrier",
        "logistics",
        "fulfillment",
    ],
)

# ==========================================================
# REVIEW
# ==========================================================

REVIEW = BusinessConcept(
    canonical_name="review",
    description="Customer feedback.",
    keywords=[
        "review",
        "rating",
        "score",
        "feedback",
        "comment",
        "stars",
    ],
)

# ==========================================================
# SELLER
# ==========================================================

SELLER = BusinessConcept(
    canonical_name="seller",
    description="Merchant selling products.",
    keywords=[
        "seller",
        "vendor",
        "merchant",
        "supplier",
        "store",
        "shop",
    ],
)

# ==========================================================
# LOCATION
# ==========================================================

LOCATION = BusinessConcept(
    canonical_name="location",
    description="Geographical information.",
    keywords=[
        "city",
        "state",
        "country",
        "province",
        "region",
        "zipcode",
        "postalcode",
        "address",
    ],
)

# ==========================================================
# DATE
# ==========================================================

DATE = BusinessConcept(
    canonical_name="date",
    description="Date or timestamp information.",
    keywords=[
        "date",
        "datetime",
        "timestamp",
        "created",
        "ordered",
        "delivered",
        "shipped",
        "registered",
        "joined",
    ],
)

# ==========================================================
# IDENTIFIER
# ==========================================================

IDENTIFIER = BusinessConcept(
    canonical_name="identifier",
    description="Unique identifier.",
    keywords=[
        "id",
        "identifier",
        "number",
        "num",
        "code",
        "reference",
        "key",
    ],
)

# ==========================================================
# ALL CONCEPTS
# ==========================================================

BUSINESS_CONCEPTS = [
    CUSTOMER,
    ORDER,
    PRODUCT,
    PAYMENT,
    DELIVERY,
    REVIEW,
    SELLER,
    LOCATION,
    DATE,
    IDENTIFIER,
]