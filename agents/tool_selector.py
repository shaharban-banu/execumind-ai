"""
LLM-based MCP Tool Selector.

Uses Gemini to determine which MCP business tools
should be executed before the Data Intelligence Agent
performs reasoning.
"""

from typing import List

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

1. Return ONLY the required tools.
2. Select the minimum number of tools.
3. Multiple tools may be selected.
4. Never invent tool names.
5. Return valid JSON.
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
# selector = ToolSelector()

# tools = selector.select_tools(
#     "Why has revenue decreased while customer growth increased?"
# )

# print(tools)