"""
Dashboard Service.

Provides KPI summaries for the executive dashboard.
"""

from sqlalchemy import func
from mcp.tools.sales_analysis import monthly_sales
from database.database import SessionLocal
from database.models import (
    Customer,
    Order,
    Payment,
)
from pathlib import Path
from services.platform_status import get_platform_status

class DashboardService:
    """Dashboard KPI Service."""

    def get_dashboard(self,user_id:int):
        db = SessionLocal()

        try:
            total_revenue = (
                db.query(func.sum(Payment.payment_value))
                .filter(Payment.user_id==user_id)
                .scalar()
            ) or 0

            total_orders = (
                db.query(func.count(Order.order_id))
                .filter(Order.user_id==user_id)
                .scalar()
            ) or 0

            total_customers = (
                db.query(
                    func.count(
                        func.distinct(Customer.customer_master_id)
                    )
                )
                .filter(Customer.user_id==user_id)
                .scalar()
            ) or 0

            average_order_value = (
                db.query(func.avg(Payment.payment_value))
                .filter(Payment.user_id==user_id)
                .scalar()
            ) or 0

            return {
                "revenue": round(total_revenue, 2),
                "orders": total_orders,
                "customers": total_customers,
                "average_order_value": round(
                    average_order_value,
                    2,
                ),
            }

        finally:
            db.close()
    @staticmethod
    def get_revenue_history(user_id:int):
        return monthly_sales(user_id)

    #to give recent activity log
    @staticmethod
    def dataset_uploaded(user_id:int) -> bool:
        dataset_dir = Path(f"data/users/{user_id}/datasets")

        return (
            dataset_dir.exists()
            and any(dataset_dir.iterdir())
        )
    @staticmethod
    def dataset_processed(user_id:int) -> bool:

        db = SessionLocal()

        try:
            order_count = (db.query(func.count(Order.order_id))
            .filter(Order.user_id == user_id)
            .scalar()) or 0

            return order_count > 0

        finally:
            db.close()
    @staticmethod
    def forecast_ready(user_id:int) -> bool:
        return get_platform_status(user_id)["platform_ready"]

    
