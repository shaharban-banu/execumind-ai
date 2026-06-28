"""Customer Intelligence Agent"""

from utils.logger import logger

from agents.base_agent import BaseAgent
from mcp.tools.search_docs import search_docs
from schemas.customer import CustomerAnalysis
from services.context_formatter import (format_reviews,format_business_docs)

class CustomerIntelligenceAgent(BaseAgent):
    """Uses review RAG and business knowledge to analyse customer issues"""

    PROMPT_FILE="customer_agent.txt"
    RESPONSE_SCHEMA=CustomerAnalysis

    def _retrieve_context(self,question:str):
        """retrieve customer reviews and business documents"""
        return search_docs(query=question,method='faiss')
    

    def _prepare_prompt(self, question, context):
        reviews=format_reviews(context["reviews"])
        business_docs=format_business_docs(context["business_docs"])
        prompt=self.load_prompt()
        return prompt.format(question=question,
                             reviews=reviews,
                             business_docs=business_docs)

    
if __name__=="__main__":
    agent=CustomerIntelligenceAgent()
    result=agent.run("why are customers complaining about late deliveries?")
    print("\n")
    print("=" * 80)
    print("CUSTOMER ANALYSIS")
    print("=" * 80)

    print(result.model_dump_json(indent=4))