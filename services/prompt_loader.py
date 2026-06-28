"""
Prompt Loader.

Loads prompt templates used by
ExecuMind AI agents.
"""
from pathlib import Path
from utils.logger import logger

PROMPT_DIR=Path("prompts")

def load_prompt(prompt_name:str):
    """load prompt template"""

    try:
        prompt_path=PROMPT_DIR/prompt_name
        with open(prompt_path,encoding='utf-8') as f:
            prompt=f.read()

        logger.info("Loaded prompt : %s ",prompt_name)
        return prompt
    except Exception:
        logger.exception("Failed to load prompt")
        raise