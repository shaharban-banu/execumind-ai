"""
ExecuMind AI FastAPI Application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

from contextlib import asynccontextmanager
from database.database import engine
from database.models import Base


from app.api.knowledge import router as knowledge_router
from app.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    yield

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
    version="1.0.0",lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5173",  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(router)

app.include_router(knowledge_router)