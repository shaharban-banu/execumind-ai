"""
Base Agent.

Defines the common interface for all
ExecuMind AI agents.
"""
from abc import ABC,abstractmethod
from typing import Type
from pydantic import BaseModel
from services.llm_service import LLMService
from services.prompt_loader import load_prompt
from utils.logger import logger
import time
from schemas.agent_response import AgentResponse

class BaseAgent(ABC):
    """Abstract base class for all agents"""

    PROMPT_FILE: str = ""
    RESPONSE_SCHEMA: Type[BaseModel] | None = None

    def __init__(self,llm_service:LLMService|None=None):
        self.llm=llm_service or LLMService()

    @abstractmethod
    def _retrieve_context(self,question:str):
        """
        Retrieve all evidence required
        for answering the question.

        Returns
        -------
        dict
            Retrieved context.
        """
    @abstractmethod
    def _prepare_prompt(self,question:str,context:dict):
        """
        Build the final prompt.

        Returns
        -------
        str
            Formatted prompt.
        """
    def _generate(self,prompt:str):
        """
        Generate structured response
        using the configured LLM."""
        if self.RESPONSE_SCHEMA is None:
            raise  ValueError("RESPONSE_SCHEMA is not configured")
        logger.info("Generating response using GEMINI...")

        return self.llm.generate(prompt=prompt,response_schema=self.RESPONSE_SCHEMA)
    
    # def _calculate_confidence(self,context: dict) :
    #     """
    #     Calculate agent confidence.

    #     Default implementation.
    #     """

    #     return 1.0

    def run(self,question:str):
        """
        Execute the agent
        Args:
                question:
                    User question.

            Returns:
                dict:
                    Agent response.
        """
        start_time=time.perf_counter()
        try:
            logger.info("Running %s ",self.__class__.__name__)
            context=self._retrieve_context(question)
            prompt=self._prepare_prompt(question,context)
            result=self._generate(prompt)
            execution_time=round(time.perf_counter()-start_time,2)
            #confidence = self._calculate_confidence(context)

            logger.info("%s completed successfully ",self.__class__.__name__)
            return AgentResponse(
                agent_name=self.__class__.__name__,
                execution_time=execution_time,
                #confidence=confidence,
                result=result
            )
        except Exception:
            logger.exception("%s failed ",self.__class__.__name__)
            raise
    def load_prompt(self):
        """
        Load the prompt template for
        the current agent."""
        if not self.PROMPT_FILE:
            raise ValueError("PROMPT_FILE is not configured")
        return load_prompt(self.PROMPT_FILE)