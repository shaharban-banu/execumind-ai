"""
Forecast Intelligence Agent.

Analyzes future business trends using forecasting
MCP tools and produces executive insights.
"""

from agents.base_agent import BaseAgent
from schemas.forecast import ForecastAnalysis
from agents.tool_selector import ToolSelector
from mcp.tool_registry import TOOL_REGISTRY
from utils.logger import logger
from services.context_formatter import format_forecast

class ForecastAgent(BaseAgent):
    """Forecast Intelligence Agent"""

    PROMPT_FILE="forecast_agent.txt"
    RESPONSE_SCHEMA=ForecastAnalysis

    def __init__(self):
        super().__init__()
        self.tool_selector=ToolSelector()

    def _retrieve_context(self,question:str):
        """execute required mcp tools"""

        logger.info("Selecting forecast MCP tools")
        tool_names=self.tool_selector.select_tools(question)
        #print(tool_names)
        context={}
        for tool_name in tool_names:
            if not tool_name.startswith("forecast_"):
                continue
            tool=TOOL_REGISTRY.get(tool_name)
            if tool is None:
                logger.warning("unknown tool selected :%s",tool_name)
                continue
            logger.info("Executing tool %s",tool_name,)
            try:
                context[tool_name]=tool()

                print(tool_name)
                print(context[tool_name])
                
            except Exception:
                logger.exception("Tool %s failed",tool_name)
                context[tool_name]={"error":"execution failed"}
        return context
    
    def _prepare_prompt(self, question, context):
        prompt_template=self.load_prompt()
        formatted_context=[]
        for tool_name,row in context.items():
            formatted_context.append(f"""
                        ==={tool_name}===
                        {format_forecast(row)}
            """)

        return prompt_template.format(question=question,context="\n".join(formatted_context),)

if __name__=="__main__":
    agent=ForecastAgent()
    response=agent.run(  "What is the expected business performance over the next six months?"
    )

    print(response.model_dump_json(indent=4))