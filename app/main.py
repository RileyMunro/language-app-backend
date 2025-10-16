from typing import Dict
from fastapi import FastAPI
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from app.database import init_db
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle startup and shutdown events."""
    # Startup: create tables
    await init_db()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(title="Language Learning API", lifespan=lifespan)

# Include the router
app.include_router(router, prefix="/api/v1", tags=["language"])

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "Language Learning API"}

@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}