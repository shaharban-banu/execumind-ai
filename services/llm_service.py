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

import instructor
import json
from groq import Groq



load_dotenv(override=True)

class LLMService:
    """shared LLM client"""

    def __init__(self):
       
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()

        if self.provider == "gemini":

            api_key = os.getenv("GOOGLE_API_KEY")

            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found")

            self.client = genai.Client(api_key=api_key)
            self.model = "gemini-2.5-flash"

            logger.info("Gemini LLM initialised")

        elif self.provider == "groq":

            api_key = os.getenv("GROQ_API_KEY")
            print("Groq Key:", api_key[:12] + "...")

            if not api_key:
                raise ValueError("GROQ_API_KEY not found")
            self.groq_client = Groq(api_key=api_key)

            self.client = instructor.from_groq(self.groq_client)

            self.model = "llama-3.3-70b-versatile"
            #self.model ="llama-3.1-8b-instant"

            logger.info("Groq LLM initialised")

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate(self,prompt:str,response_schema:Type[BaseModel]):
        """generate LLM response"""

        try:
            # if self.use_mock:
            #     return self.mock.generate(prompt,response_schema,)
            
            if self.provider == "gemini":
                response=self.client.models.generate_content(model=self.model,
                                                            contents=prompt,
                                                            config={
                                                                "response_mime_type":"application/json",
                                                                "response_schema":response_schema,
                                                                "temperature":0
                                                            })
                logger.info("LLM response generated")
                return response.parsed
            
            elif self.provider == "groq":

                response = self.client.chat.completions.create(
                    model=self.model,
                    response_model=response_schema,
                    temperature=0,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an executive AI assistant."
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                )
                return response

        except Exception:
            logger.exception("LLM generation failed..")
            raise

    def generate_text(self, prompt: str) -> str:
            """
            Generate plain text response.
            Used for evaluation scripts where structured output
            is unnecessary.
            """

            try:

                if self.provider == "gemini":

                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=prompt,
                        config={
                            "temperature": 0,
                        },
                    )

                    logger.info("Text response generated")
                    return response.text.strip()

                elif self.provider == "groq":

                    response = self.groq_client.chat.completions.create(
                        model=self.model,
                        temperature=0,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an executive AI assistant.",
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                    )

                    logger.info("Text response generated")
                    return response.choices[0].message.content.strip()

            except Exception:
                logger.exception("LLM text generation failed.")
                raise
            