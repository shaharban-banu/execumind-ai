"""
LLM Service.

Provides a common interface for all
ExecuMind AI agents.
"""

import os
from typing import Type
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from utils.logger import logger

load_dotenv()

class LLMService:
    """shared Gemini client"""

    def __init__(self):
        api_key=os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found")
        
        self.client=genai.Client(api_key=api_key)
        self.model="gemini-2.5-flash"
        logger.info("GEMINI LLM initialised")

    def generate(self,prompt:str,response_schema:Type[BaseModel]):
        """generate LLM response"""

        try:
            response=self.client.models.generate_content(model=self.model,
                                                         contents=prompt,
                                                         config={
                                                             "response_mime_type":"application/json",
                                                             "response_schema":response_schema,
                                                             "temperature":0
                                                         })
            logger.info("LLM response generated")
            return response.parsed
        except Exception:
            logger.exception("LLM generation failed..")
            raise
        