"""
database/models.py

SQLAlchemy models for the canonical e-commerce schema.
"""

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ==========================================================
# Customers
# ==========================================================

class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )
    customer_master_id = Column(String)
    
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)

    customer_city = Column(String)
    customer_state = Column(String)
    customer_country = Column(String)

    customer_created_date = Column(DateTime)


# ==========================================================
# Orders
# ==========================================================

class Order(Base):

    __tablename__ = "orders"

    order_id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )

    customer_id = Column(
        String,
        ForeignKey("customers.customer_id"),
        nullable=False,
        index=True,
    )

    order_date = Column(DateTime)

    order_status = Column(String)

    order_value = Column(Float)

    estimated_delivery_date = Column(DateTime)

    delivered_date = Column(DateTime)


# ==========================================================
# Products
# ==========================================================

class Product(Base):

    __tablename__ = "products"

    product_id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )

    product_name = Column(String)

    product_category = Column(
        String,
        index=True,
    )

    price = Column(Float)

    weight = Column(Float)


# ==========================================================
# Sellers
# ==========================================================

class Seller(Base):

    __tablename__ = "sellers"

    seller_id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )

    seller_name = Column(String)

    seller_city = Column(String)

    seller_state = Column(String)


# ==========================================================
# Order Items
# ==========================================================

class OrderItem(Base):

    __tablename__ = "order_items"

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),
        nullable=False,
        index=True,
    )

    order_item_id = Column(
        String,
        nullable=False,
    )

    product_id = Column(
        String,
        ForeignKey("products.product_id"),
        nullable=False,
        index=True,
    )

    seller_id = Column(
        String,
        ForeignKey("sellers.seller_id"),
        index=True,
    )

    quantity = Column(Integer)

    unit_price = Column(Float)

    freight_cost = Column(Float)

    order_item_value = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(
            "order_id",
            "order_item_id",
        ),
    )


# ==========================================================
# Payments
# ==========================================================

class Payment(Base):

    __tablename__ = "payments"

    payment_id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),
        nullable=False,
        index=True,
    )

    payment_method = Column(String)

    payment_value = Column(Float)

    payment_installments = Column(Integer)


# ==========================================================
# Reviews
# ==========================================================

class Review(Base):

    __tablename__ = "reviews"

    review_id = Column(String,nullable=False,)

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),nullable=False, index=True,)

    review_score = Column(Integer)

    review_title = Column(String)

    review_comment = Column(String)

    review_date = Column(DateTime)

    review_text=Column(String)

    __table_args__ = (
        PrimaryKeyConstraint(
            "review_id",
            "order_id",
        ),
    )


# ==========================================================
# Deliveries
# ==========================================================

class Delivery(Base):

    __tablename__ = "deliveries"

    delivery_id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),
        nullable=False,
        index=True,
    )

    carrier = Column(String)

    shipped_date = Column(DateTime)

    delivered_date = Column(DateTime)

    delivery_status = Column(String)

    freight_cost = Column(Float)