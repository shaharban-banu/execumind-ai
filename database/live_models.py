"""
Live Mirror Models for Data Simulator.
 
Mirrors the four streaming tables (orders, order_items,
reviews, payments) without foreign key constraints so the
simulator can insert rows independently at any speed.
 
Static tables (customers, sellers, products, geolocation,
category_translations) are NOT mirrored — agents join to
the originals directly during simulation.
"""
from sqlalchemy import (Column,Integer,String,Float,PrimaryKeyConstraint)
from sqlalchemy.orm import declarative_base
LiveBase=declarative_base()

class LiveOrder(LiveBase):
    """
    Live mirror of the orders table.
 
    Receives one row per order as the simulator
    replays olist_orders_dataset chronologically.
    No FK to customers — join to static customers
    table at query time.
    """
    __tablename__="live_orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String)
    order_status = Column(String)
    order_purchase_timestamp = Column(String)
    order_approved_at = Column(String)
    order_delivered_carrier_date = Column(String)
    order_delivered_customer_date = Column(String)
    order_estimated_delivery_date = Column(String)

class LiveOrderItem(LiveBase):
    """
    Live mirror of the order_items table.
 
    Inserted in the same simulator tick as the
    matching LiveOrder row. Provides revenue,
    freight, product, and seller signals.
    No FK constraints — simulator manages ordering.
    """
    __tablename__="live_order_item"

    order_id = Column(String)
    order_item_id = Column(Integer)
    product_id = Column(String)
    seller_id = Column(String)
    shipping_limit_date = Column(String)
    price = Column(Float)
    freight_value = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(
            "order_id",
            "order_item_id"
        ),
    )

class LiveReview(LiveBase):
    """
    Live mirror of the reviews table.
 
    Inserted with a realistic delay after the order
    to simulate reviews arriving days post-delivery.
    This is the key sentiment signal for the
    Customer Intelligence Agent in live mode.
    No FK constraints.
    """

    __tablename__="live_reviews"

    review_id = Column(String, primary_key=True)
    order_id = Column(String)
    review_score = Column(Integer)
    review_comment_title = Column(String)
    review_comment_message = Column(String)
    review_creation_date = Column(String)
    review_answer_timestamp = Column(String)

class LivePayment(LiveBase):
    """
    Live mirror of the payments table.
 
    Inserted in the same simulator tick as the
    matching LiveOrder row. Provides payment type
    distribution and revenue totals for KPI cards.
    No FK constraints.
    """

    __tablename__="live_payments"

    order_id = Column(String)
    payment_sequential = Column(Integer)
    payment_type = Column(String)
    payment_installments = Column(Integer)
    payment_value = Column(Float)

    __table_args__ = (PrimaryKeyConstraint("order_id","payment_sequential"),)

class SimulatorEvent(LiveBase):
    """
    Simulator state and event log.
 
    Every significant simulator action is logged here:
    start, pause, reset, speed change, anomaly injection.
    The FastAPI /simulator/status endpoint reads from
    this table to report current simulation state to
    the React Live Feed page.
    """

    __tablename__="simulator_events"

    id=Column(Integer,primary_key=True,autoincrement=True)
    
    # Type of event: start | pause | reset | speed_change | anomaly_injected
    event_type=Column(String,nullable=False)
    timestamp=Column(String,nullable=False)
    orders_inserted=Column(Integer,default=0)

    # Replay speed at time of event: slow | normal | fast
    current_speed=Column(String,default='normal')

    anomaly_injected=Column(Integer,default=0)

    # Human-readable description: e.g. "Injected delay spike in SP state"
    notes=Column(String,default="")