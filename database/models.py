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
    String,Text,Boolean
)
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()

# ==========================================================
# Users
# ==========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True,)

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(20),
        nullable=False,
        default="executive",
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")),
        nullable=False,
    )

# ==========================================================
# Datasets
# ==========================================================

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")),
        nullable=False,
    )

    versions = relationship(
        "DatasetVersion",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )

# ==========================================================
# Dataset Versions
# ==========================================================

class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id"),
        nullable=False,
        index=True,
    )

    version_number = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String(30),
        default="uploaded",
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    dataset = relationship(
        "Dataset",
        back_populates="versions",
    )

    files = relationship(
        "DatasetFile",
        back_populates="version",
        cascade="all, delete-orphan",
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")),
        nullable=False,
    )

# ==========================================================
# Dataset Files
# ==========================================================

class DatasetFile(Base):
    """
    Represents an individual file belonging to a dataset version.

    A dataset version may contain multiple files, such as
    customers, orders, products, payments, and reviews.
    """

    __tablename__ = "dataset_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    version_id = Column(
        Integer,
        ForeignKey("dataset_versions.id"),
        nullable=False,
        index=True,
    )

    file_name = Column(
        String(255),
        nullable=False,
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(
            ZoneInfo("Asia/Kolkata")
        ),
        nullable=False,
    )

    version = relationship(
        "DatasetVersion",
        back_populates="files",
    )
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
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User")


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
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User")


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

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User")


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
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User")


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

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User")


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

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User")

# ==========================================================
# Executive recommendation for frontend
# ==========================================================
class ExecutiveRecommendation(Base):
    __tablename__ = "executive_recommendations"

    id = Column(Integer, primary_key=True, index=True)

    priority = Column(String(20), nullable=False)

    action = Column(Text, nullable=False)

    rationale = Column(Text, nullable=False)

    executive_summary = Column(Text)

    key_findings = Column(Text)      # JSON string

    business_risks = Column(Text)    # JSON string

    evidence = Column(Text)          # JSON string

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")),
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User")