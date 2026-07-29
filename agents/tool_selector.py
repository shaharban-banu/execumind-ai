"""
LLM-based MCP Tool Selector.

Uses Gemini to determine which MCP business tools
should be executed before the Data Intelligence Agent
performs reasoning.
"""

from typing import List
import os
from pydantic import BaseModel, Field

from services.llm_service import LLMService
from utils.logger import logger


class ToolSelection(BaseModel):
    """Structured response returned by Gemini."""

    tools: List[str] = Field(
        description="List of MCP tool names to execute."
    )


class ToolSelector:
    """
    Uses Gemini to decide which MCP tools are required
    for an executive question.
    """

    TOOL_DESCRIPTIONS = """
Sales
-----
sales_summary
    Overall revenue, order count and average order value.

monthly_sales
    Monthly revenue trend.

sales_by_state
    Revenue by customer state.

sales_by_category
    Revenue by product category.

Customers
---------
customer_summary
    Overall customer statistics.

customer_growth
    Monthly customer acquisition.

repeat_customer_rate
    Repeat customer analysis.

customers_by_state
    Customer distribution by state.

Delivery
--------
delivery_summary
    Overall delivery performance.

late_delivery_rate
    Percentage of delayed deliveries.

delivery_by_state
    Delivery performance grouped by state.

order_status_distribution
    Distribution of order status.

Sellers
-------
seller_summary
    Overall seller statistics.

top_sellers
    Highest revenue sellers.

seller_revenue
    Revenue by seller.

seller_delivery_performance
    Seller delivery quality.

Products
--------
product_summary
    Product statistics.

category_performance
    Revenue by category.

top_products
    Best selling products.

product_price_statistics
    Product price statistics.

Payments
--------
payment_summary
    Overall payment statistics.

payment_methods
    Payment method distribution.

installment_analysis
    Installment usage.

payment_value_distribution
    Payment value statistics.

Forecast
--------

forecast_revenue
    Predicts future revenue only. Never use for historical analysis or reporting.

forecast_orders
    Predicts future order volume only. Never use for historical order statistics.

forecast_customer_growth
    Predicts future customer growth only.

forecast_average_order_value
    Predicts future average order value only.
"""

    TOOL_SELECTION_PROMPT = """
You are an executive analytics planner.

Your task is NOT to answer the question.

Your only task is to determine which MCP business
tools should be executed.

Executive Question:

{question}

Available Tools:

{tools}

Rules:

1. Return ONLY the minimum number of tools required to answer the question.

2. Select forecast tools ONLY if the question explicitly asks about future predictions, forecasts, projections, or expected future values.

Examples of forecast questions:
- Forecast next month's revenue
- Predict future customer growth
- What will sales be next quarter?
- Expected order volume next month

3. Do NOT select any forecast tool for historical or descriptive questions.

Examples of historical questions:
- Show monthly sales
- Analyze sales trend
- Sales by state
- Customer summary
- Payment statistics
- Delivery performance

4. Historical trend analysis is NOT forecasting.

5. Do NOT select additional summary tools unless they are necessary to answer the question.

6. Never invent tool names.

7. Return only valid JSON in the format:

{{
  "tools": [
    "tool_name"
  ]
}}
"""

    def __init__(self) -> None:
        self.llm = LLMService()

    def select_tools(self, question: str) -> List[str]:
        """
        Determine which MCP tools should be executed.

        Args:
            question:
                Executive business question.

        Returns:
            List of MCP tool names.
        """
        # Offline testing
        if os.getenv("USE_MOCK_LLM", "False").lower() == "true":

            q = question.lower()

            if any(word in q for word in ["forecast", "predict", "future"]):
                return [
                    "forecast_revenue",
                    "forecast_orders",
                ]

            if any(word in q for word in ["delivery", "shipping", "late"]):
                return [
                    "delivery_summary",
                    "late_delivery_rate",
                ]

            if any(word in q for word in ["customer", "review", "satisfaction"]):
                return [
                    "customer_summary",
                    "repeat_customer_rate",
                ]

            return [
                "sales_summary",
                "monthly_sales",
            ]

        # Existing Gemini/Groq code
        logger.info("Selecting MCP tools...")

        prompt = self.TOOL_SELECTION_PROMPT.format(
            question=question,
            tools=self.TOOL_DESCRIPTIONS,
        )

        response = self.llm.generate(
            prompt=prompt,
            response_schema=ToolSelection,
        )

        logger.info("Selected tools: %s", response.tools)
        return response.tools

#test--------
if __name__ == "__main__":
    selector = ToolSelector()
    tools = selector.select_tools(
        "Predict future customer growth and orders"
    )
    print(tools)