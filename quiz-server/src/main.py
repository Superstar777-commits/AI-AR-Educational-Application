"""
    Entry point for the application
    Handles all the mounting for the routers, logs, port, CORS policy
"""

from typing import Union, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
import sys
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# IMPORTANT: ensure 'src' is in Python path
# this helps relative imports within the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import fastapi routers
from src.api.routers import user_router
from src.api.routers import question_router
from src.api.routers import quiz_router
from src.api.routers import analysis_router
from src.api.routers import answer_router
from src.api.routers import log_router
from src.api.routers import topics_router
from src.api.routers import schools_router
from src.api.routers import qopts_router
from src.api.routers import ml_route

# import db initialization function and metadata object
from src.core.database import init_db

app_state: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event: intialize db, load ML models
    logger.info("Application starting up (SQLAlchemy Core)...")

    try:
        # 1. Initialize database (create tables if they don't exist)
        await init_db()
        logger.info("Database initialization complete.")

        # 2. Load ML models on startup using the ModelManager Singleton
        # model_manager = ModelManager()
        # app_state["model_manager"] = model_manager # Store it if needed, though Singleton provides access
        logger.info("ML models loaded (or initialized via ModelManager).")

    except Exception as e:
        logger.error(f"Error during application startup: {e}", exc_info=True)
        # Re-raise the exception to prevent the application from starting in a bad state
        # fastapi dev / uvicorn will likely catch this and signal a failure
        raise # Critical: Re-raise to prevent partial startup in a broken state

    yield # Application is ready to receive requests

    # Shutdown event: Clean up resources
    logger.info("Application shutting down...")
    # Add any specific cleanup logic here if necessary for global resources
    # (e.g., explicitly clearing model_manager if it held external resources not managed by its own lifecycle)
    # Most cleanup for DB sessions is handled by get_db dependency.
    logger.info("Application shutdown complete.")


app = FastAPI(
    title="Quiz App API",
    description="Backend for the Quiz app",
    version="0.1.0",
    lifespan=lifespan
)

# add your frontend's url
origin = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# include routers
app.include_router(user_router.router)
app.include_router(question_router.router)
app.include_router(quiz_router.router)
app.include_router(answer_router.router)
app.include_router(analysis_router.router)
app.include_router(log_router.router)
app.include_router(topics_router.router)
app.include_router(schools_router.router)
app.include_router(qopts_router.router)
app.include_router(ml_route.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend"}