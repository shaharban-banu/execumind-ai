"""
Data Intelligence Agent.

Analyzes structured business data using MCP business
tools and produces executive insights.
"""

from agents.base_agent import BaseAgent
from schemas.data import DataAnalysis
from agents.tool_selector import ToolSelector
from mcp.tool_registry import TOOL_REGISTRY
from utils.logger import logger
from services.context_formatter import format_sql_results

class DataAgent(BaseAgent):
    PROMPT_FILE="data_agent.txt"
    RESPONSE_SCHEMA=DataAnalysis

    def __init__(self):
        super().__init__()
        self.tool_selector=ToolSelector()

    def _retrieve_context(self,question:str,mode:str="historical"):
        """execute required mcp tools"""

        logger.info("Selecting MCP tools")

        if mode=="executive":
            tool_names=[
                "sales_summary",
                "customer_summary",
                "delivery_summary",
                "category_performance",
                "payment_summary"
            ]
        else:
            tool_names=self.tool_selector.select_tools(question)
        #print(tool_names)
        context={}
        for tool_name in tool_names:
            tool=TOOL_REGISTRY.get(tool_name)

            if tool is None:
                logger.warning("unknown tool selected :%s",tool_name)
                continue
            # if tool.startswith("forecast_"):
            #     continue
            logger.info("Executing tool %s",tool_name,)
            try:
                context[tool_name]=tool(mode=mode)
            except Exception:
                logger.exception("Tool %s failed",tool_name)
                context[tool_name]=[]
        return context
    
    def _prepare_prompt(self, question, context):
        prompt_template=self.load_prompt()
        formatted_context=[]
        for tool_name,row in context.items():
            formatted_context.append(f"""
                        ==={tool_name}===
                        {format_sql_results(row)}
            """)

        return prompt_template.format(question=question,context="\n".join(formatted_context),)

if __name__=="__main__":
    agent=DataAgent()
    response=agent.run(
       "Generate a complete executive business report."
        )

    print(response.model_dump_json(indent=4))