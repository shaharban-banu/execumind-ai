"""
Registry of MCP business capability tools.

Maps business capabilities to executable functions.
The Data Agent uses this registry to invoke tools
without importing every module directly.
"""
from mcp.tools.sales_analysis import (sales_summary,sales_by_state,monthly_sales,sales_by_category)
from mcp.tools.customer_metrics import (customer_summary,customer_growth,customers_by_state,repeat_customer_rate)
from mcp.tools.delivery_analysis import ( delivery_summary,delivery_by_state,late_delivery_rate)
from mcp.tools.seller_analysis import (seller_summary,top_sellers)
from mcp.tools.product_analysis import (product_summary,category_performance)
from mcp.tools.payment_analysis import (payment_summary,payment_methods)

from mcp.tools.forecast_revenue import (forecast_revenue)
from mcp.tools.forecast_orders import (forecast_orders)
from mcp.tools.forecast_customer_growth import (forecast_customer_growth)
from mcp.tools.forecast_aov import (forecast_average_order_value)

TOOL_REGISTRY={
     "sales_summary": sales_summary,
    "monthly_sales": monthly_sales,
    "sales_by_state": sales_by_state,
    "sales_by_category": sales_by_category,

    "customer_summary": customer_summary,
    "customer_growth": customer_growth,
    "repeat_customer_rate": repeat_customer_rate,
    "customers_by_state": customers_by_state,

    "delivery_summary": delivery_summary,
    "late_delivery_rate": late_delivery_rate,
    "delivery_by_state": delivery_by_state,

    "seller_summary": seller_summary,
    "top_sellers": top_sellers,

    "product_summary": product_summary,
    "category_performance": category_performance,

    "payment_summary": payment_summary,
    "payment_methods": payment_methods,

    "forecast_revenue": forecast_revenue,
    "forecast_orders": forecast_orders,
    "forecast_customer_growth": forecast_customer_growth,
    "forecast_average_order_value": forecast_average_order_value,

}