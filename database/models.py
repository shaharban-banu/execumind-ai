from sqlalchemy import (Column,Integer,String,Float,ForeignKey,PrimaryKeyConstraint)
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Customer(Base):
    __tablename__="customers"
    customer_id=Column(String,primary_key=True)
    customer_unique_id = Column(String)
    customer_zip_code_prefix = Column(Integer)
    customer_city = Column(String)
    customer_state = Column(String)

class Order(Base):

    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)

    customer_id = Column(
        String,
        ForeignKey("customers.customer_id")
    )

    order_status = Column(String)
    order_purchase_timestamp = Column(String)
    order_approved_at = Column(String)
    order_delivered_carrier_date = Column(String)
    order_delivered_customer_date = Column(String)
    order_estimated_delivery_date = Column(String)

class Product(Base):

    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    product_category_name = Column(String)
    product_name_lenght = Column(Integer)
    product_description_lenght = Column(Integer)
    product_photos_qty = Column(Integer)
    product_weight_g = Column(Float)
    product_length_cm = Column(Float)
    product_height_cm = Column(Float)
    product_width_cm = Column(Float)

class Review(Base):

    __tablename__ = "reviews"

    review_id = Column(String, primary_key=True)

    order_id = Column(
        String,
        ForeignKey("orders.order_id")
    )

    review_score = Column(Integer)
    review_comment_title = Column(String)
    review_comment_message = Column(String)
    review_creation_date = Column(String)
    review_answer_timestamp = Column(String)

class Seller(Base):

    __tablename__ = "sellers"

    seller_id = Column(String, primary_key=True)
    seller_zip_code_prefix = Column(Integer)
    seller_city = Column(String)
    seller_state = Column(String)

class Payment(Base):

    __tablename__ = "payments"

    order_id = Column(
        String,
        ForeignKey("orders.order_id")
    )

    payment_sequential = Column(Integer)
    payment_type = Column(String)
    payment_installments = Column(Integer)
    payment_value = Column(Float)

    __table_args__ = (PrimaryKeyConstraint("order_id","payment_sequential"),)

class OrderItem(Base):

    __tablename__ = "order_items"

    order_id = Column(
        String,
        ForeignKey("orders.order_id")
    )

    order_item_id = Column(Integer)

    product_id = Column(
        String,
        ForeignKey("products.product_id")
    )

    seller_id = Column(
        String,
        ForeignKey("sellers.seller_id")
    )

    shipping_limit_date = Column(String)

    price = Column(Float)

    freight_value = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(
            "order_id",
            "order_item_id"
        ),
    )

class Geolocation(Base):

    __tablename__ = "geolocation"

    geolocation_zip_code_prefix = Column(Integer)
    geolocation_lat = Column(Float)
    geolocation_lng = Column(Float)
    geolocation_city = Column(String)
    geolocation_state = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint(
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng"
        ),
    )