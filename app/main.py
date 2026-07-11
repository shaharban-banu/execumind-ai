"""
ExecuMind AI FastAPI Application.
"""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="ExecuMind AI",
    description="""
## Multi-Agent Executive Intelligence Platform

ExecuMind AI helps business executives answer:

• What happened?

• Why did it happen?

• What will happen next?

• What should we do?

### Workflow

User Question

↓

Planner Agent

↓

Executive Orchestrator

↓

Customer Agent / Data Agent / Forecast Agent

↓

Executive Intelligence Report
""",
    version="1.0.0",
)

app.include_router(router)