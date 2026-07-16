"""
synonyms.py

Business vocabulary normalization used by the Semantic Mapper.

This module normalizes different business terms into a common vocabulary
before applying fuzzy matching or semantic embeddings.
"""

# ==========================================================
# CUSTOMER
# ==========================================================

CUSTOMER_SYNONYMS = {
    "cust": "customer",
    "client": "customer",
    "buyer": "customer",
    "consumer": "customer",
    "shopper": "customer",
    "user": "customer",
    "account": "customer",
    "member": "customer",
    "email":"customer_email",
    "email_address":"customer_email",
    "mail":"customer_email",
    "city":"customer_city",
    "customer_city":"customer_city",
    "state":"customer_state",
    "province":"customer_state",
    "signup_date":"customer_created_date",
    "registration_date":"customer_created_date",
    "created_date":"customer_created_date",
    "join_date":"customer_created_date",
    "customer_unique_id": "customer_master_id",
    "buyer_unique_id": "customer_master_id",
    "client_id": "customer_master_id",
    "member_id": "customer_master_id",
    "master_customer_id": "customer_master_id",
}

# ==========================================================
# ORDER
# ==========================================================

ORDER_SYNONYMS = {
    "sale": "order",
    "sales": "order",
    "purchase": "order",
    "transaction": "order",
    "booking": "order",
    "invoice": "order",

    "order_purchase_timestamp": "order_date",
    "purchase_timestamp": "order_date",
    "purchase_date": "order_date",
}

# ==========================================================
# PRODUCT
# ==========================================================

PRODUCT_SYNONYMS = {
    "item": "product",
    "goods": "product",
    "merchandise": "product",
    "sku": "product",
    "article": "product",
    "category":"product_category",
    "product_category":"product_category",
    "category_name":"product_category",
    "price":"price",
    "unit_price":"price",
    "selling_price":"price",
    "product_price":"price",
    "weight":"weight",
    "item_weight":"weight",
}

# ==========================================================
# SELLER
# ==========================================================

SELLER_SYNONYMS = {
    "vendor": "seller",
    "merchant": "seller",
    "supplier": "seller",
    "store": "seller",
    "shop": "seller",
}

# ==========================================================
# PAYMENT
# ==========================================================

PAYMENT_SYNONYMS = {
    "payment": "payment",
    "billing": "payment",
    "invoice_payment": "payment",
    "transaction_payment": "payment",
    "payment_amount":"payment_value",
    "amount":"payment_value",
    "paid_amount":"payment_value",
    "payment_value":"payment_value",
    "installments":"payment_installments",
    "emi":"payment_installments",
    "payment_installments":"payment_installments",
    "payment_type": "payment_method",
    "payment_method": "payment_method",
}

# ==========================================================
# REVIEW
# ==========================================================

REVIEW_SYNONYMS = {
    # Entity aliases
    "rating": "review",
    "ratings": "review",
    "feedback": "review",
    "comment": "review",
    "comments": "review",
    "testimonial": "review",

    # Fields
    "review_score": "review_score",
    "score": "review_score",
    "rating_score": "review_score",

    "review_title": "review_title",
    "review_comment_title": "review_title",
    "title": "review_title",

    "review_comment": "review_comment",
    "review_comment_message": "review_comment",
    "message": "review_comment",
    "review_message": "review_comment",

    # Combined field (generated later in Transformer)
    "review_text": "review_text",
}

# ==========================================================
# DELIVERY
# ==========================================================

DELIVERY_SYNONYMS = {
    "delivery_id": "delivery_id",

    "order_id": "order_id",

    "carrier": "carrier",
    "carrier_name": "carrier",
    "shipping_partner": "carrier",
    "courier": "carrier",

    "shipped_date": "shipped_date",
    "shipping_date": "shipped_date",
    "dispatch_date": "shipped_date",

    "delivered_date": "delivered_date",
    "delivery_date": "delivered_date",

    "delivery_status": "delivery_status",
    "status": "delivery_status",

    "freight_cost": "freight_cost",
    "shipping_cost": "freight_cost",
    "delivery_charge": "freight_cost",

    "order_delivered_customer_date": "delivered_date",
    "delivery_date": "delivered_date",
    "delivered_customer_date": "delivered_date",

    "order_estimated_delivery_date": "estimated_delivery_date",
}

# ==========================================================
# IDENTIFIERS
# ==========================================================

IDENTIFIER_SYNONYMS = {
    "identifier": "id",
    "number": "id",
    "num": "id",
    "code": "id",
    "key": "id",
    "reference": "id",
    "ref": "id",
}

# ==========================================================
# DATES
# ==========================================================

DATE_SYNONYMS = {
    "created": "date",
    "creation": "date",
    "purchased": "date",
    "ordered": "date",
    "joined": "date",
    "registered": "date",
    "signup": "date",
    "timestamp": "date",
    "datetime": "date",
}

# ==========================================================
# LOCATION
# ==========================================================

LOCATION_SYNONYMS = {
    "town": "city",
    "municipality": "city",
    "province": "state",
    "region": "state",
    "nation": "country",
}

# ==========================================================
# STATUS
# ==========================================================

STATUS_SYNONYMS = {
    "state": "status",
    "condition": "status",
}

# ==========================================================
# QUANTITY
# ==========================================================

QUANTITY_SYNONYMS = {
    "qty": "quantity",
    "count": "quantity",
    "units": "quantity",
}

# ==========================================================
# PRICE / VALUE
# ==========================================================

VALUE_SYNONYMS = {
    "amount": "value",
    "total": "value",
    "cost": "value",
    "price": "price",
    "charge": "value",
    "fee": "value",
}

ORDER_ITEMS_SYNONYMS={
    "unit_price":"unit_price",
    "unit_price_inr":"unit_price",
    "price":"unit_price",
    "freight_cost":"freight_cost",
    "freight_cost_inr":"freight_cost",
    "shipping_cost":"freight_cost",
    "line_total":"order_item_value",
    "line_total_inr":"order_item_value",
    "subtotal":"order_item_value",
    "item_total":"order_item_value",

    
}


# ==========================================================
# MASTER DICTIONARY
# ==========================================================

SYNONYMS = (
    CUSTOMER_SYNONYMS
    | ORDER_SYNONYMS
    | PRODUCT_SYNONYMS
    | SELLER_SYNONYMS
    | PAYMENT_SYNONYMS
    | REVIEW_SYNONYMS
    | DELIVERY_SYNONYMS
    | IDENTIFIER_SYNONYMS
    | DATE_SYNONYMS
    | LOCATION_SYNONYMS
    | STATUS_SYNONYMS
    | QUANTITY_SYNONYMS
    | VALUE_SYNONYMS
    | ORDER_ITEMS_SYNONYMS
)