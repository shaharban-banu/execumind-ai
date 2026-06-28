from pydantic import BaseModel,Field

from typing import Any

class AgentResponse(BaseModel):

    agent_name: str=Field(description="Name of the agent.")

    execution_time: float=Field(description="Execution time in seconds")

    #confidence: float=Field(description="overall confidence score.")

    result: Any=Field(description="Agent specific response")