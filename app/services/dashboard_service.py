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

class DashboardService:
    """Dashboard KPI Service."""

    def get_dashboard(self):
        db = SessionLocal()

        try:
            total_revenue = (
                db.query(func.sum(Payment.payment_value))
                .scalar()
            ) or 0

            total_orders = (
                db.query(func.count(Order.order_id))
                .scalar()
            ) or 0

            total_customers = (
                db.query(
                    func.count(
                        func.distinct(Customer.customer_master_id)
                    )
                )
                .scalar()
            ) or 0

            average_order_value = (
                db.query(func.avg(Payment.payment_value))
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
    def get_revenue_history():
        return monthly_sales()
