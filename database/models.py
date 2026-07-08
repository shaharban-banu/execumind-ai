from sqlalchemy import (Column,Integer,String,Float,ForeignKey,PrimaryKeyConstraint,DateTime)
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Customer(Base):
    __tablename__="customers"
    customer_id=Column(String,primary_key=True,nullable=False,index=True)
    customer_unique_id = Column(String)
    zip_code = Column(String)
    city = Column(String)
    state = Column(String)

class Order(Base):

    __tablename__ = "orders"

    order_id = Column(String, primary_key=True,nullable=False,index=True)

    customer_id = Column(
        String,
        ForeignKey("customers.customer_id"),nullable=False,index=True
    )

    order_status = Column(String)
    order_date = Column(DateTime,nullable=False,index=True)
    approved_date = Column(DateTime)
    carrier_delivery_date = Column(DateTime)
    delivered_date = Column(DateTime)
    estimated_delivery_date = Column(DateTime)

class Product(Base):

    __tablename__ = "products"

    product_id = Column(String, primary_key=True,nullable=False,index=True)
    category = Column(String,index=True)
    product_name_length = Column(Integer)
    product_description_length = Column(Integer)
    photos_count = Column(Integer)
    weight = Column(Float)
    length = Column(Float)
    height = Column(Float)
    width = Column(Float)

class Review(Base):

    __tablename__ = "reviews"

    review_id = Column(String, primary_key=True,nullable=False,index=True)

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),nullable=False,index=True
    )

    review_score = Column(Integer)
    review_title = Column(String)
    review_text = Column(String)
    review_creation_date = Column(DateTime)
    review_answer_date = Column(DateTime)

class Seller(Base):

    __tablename__ = "sellers"

    seller_id = Column(String, primary_key=True,nullable=False,index=True)
    zip_code = Column(String)
    city = Column(String)
    state = Column(String)

class Payment(Base):

    __tablename__ = "payments"

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),nullable=False,index=True
    )

    payment_sequence = Column(String,nullable=False)
    payment_type = Column(String)
    installments = Column(Integer)
    sales_amount = Column(Float,nullable=False)

    __table_args__ = (PrimaryKeyConstraint("order_id","payment_sequence"),)

class OrderItem(Base):

    __tablename__ = "order_items"

    order_id = Column(String,ForeignKey("orders.order_id"),nullable=False,index=True)
    order_item_id = Column(String,nullable=False)
    product_id = Column(String,ForeignKey("products.product_id"),nullable=False,index=True)
    seller_id = Column(String,ForeignKey("sellers.seller_id"),index=True)
    shipping_limit_date = Column(DateTime)
    item_price = Column(Float,nullable=False)
    freight_cost = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(
            "order_id",
            "order_item_id"
        ),
    )

class Geolocation(Base):

    __tablename__ = "geolocation"

    zip_code = Column(String,nullable=False)
    latitude = Column(Float,nullable=False)
    longitude = Column(Float,nullable=False)
    city = Column(String)
    state = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint(
            "zip_code",
            "latitude",
            "longitude"
        ),
    )

class CategoryTranslation(Base):
    __tablename__="category_translation"

    category=Column(String,primary_key=True,nullable=False,index=True)
    category_english=Column(String)