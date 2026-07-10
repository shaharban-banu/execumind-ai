"""
LLM-based retrieval strategy router.
"""
from utils.logger import logger
from rag.config.rag_config import RAGConfig
from rag.routings.base_router import BaseRouter

class LLMRouter(BaseRouter):
    """
    LLM-based retrieval strategy router.

    Uses an LLM to select the best retrieval strategy.
    """
    def __init__(self,llm,config:RAGConfig):
        """
        Initialize router.
        """
        self.llm = llm
        self.config = config
    
    def select_strategy(self, query:str):
        """
        Select retrieval strategy.
        """
        if not self.config.router_enabled:
            return self.config.default_retriever
        
        prompt=self._build_prompt(query)

        response = self.llm.invoke(prompt)

        strategy = response.content.strip().lower()

        if strategy not in self.config.available_retrievers:
            logger.warning(
                "Invalid strategy '%s'. Falling back to '%s'.",strategy,self.config.default_retriever,
                )
            return self.config.default_retriever

        logger.info("LLM selected '%s' strategy.",strategy,)

        return strategy

    def _build_prompt(self,query: str,):
        """
        Build routing prompt.
        """

        strategies = ", ".join(self.config.available_retrievers)

        return f"""
You are an expert Retrieval Strategy Router.

Available retrieval strategies:

{strategies}

Choose ONLY ONE strategy.

Guidelines:

semantic
- General semantic similarity search.

bm25
- Exact identifiers.
- Order IDs.
- Product names.
- Invoice numbers.

hybrid
- Mixed keyword + semantic search.

hyde
- Reasoning questions.
- Recommendations.
- Strategic analysis.
- "How", "Why", "What should".

User Question:

{query}

Return ONLY the strategy name.
"""
