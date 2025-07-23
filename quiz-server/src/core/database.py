"""
    Handles DB connections and creating the tables (models)
"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, Session # Use Session for synchronous context
from starlette.concurrency import run_in_threadpool # Essential for running sync code in async app
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager

from .config import settings
import asyncio # For the async startup check

# The DATABASE_URL is defined in your .env and loaded via config.py
# Ensure it uses the 'mysql+pymysql' dialect
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the synchronous engine
# pool_pre_ping=True helps maintain connections for long-running apps
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)

# Create a synchronous sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# MetaData object to hold Table definitions
metadata = MetaData()

Base = declarative_base()

# --- Dependency to get a synchronous database session in an async context ---
@asynccontextmanager
async def get_db():
    """Dependency to get a synchronous database session.
    It yields the session and ensures it's closed in the same thread.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Crucial: Close the session in the same thread it was opened.
        # run_in_threadpool ensures this blocking call doesn't block the event loop.
        await run_in_threadpool(db.close)


# --- IMPORTANT: Initialize DB (create tables) in a thread pool during startup ---
async def init_db():
    """Initializes the database: creates tables if they don't exist.
    This runs blocking SQLAlchemy Core operations (create_all) in a thread pool during startup.
    """
    print("Attempting to initialize database tables (SQLAlchemy Core)...")

    # Define a synchronous function to call create_all on MetaData
    def create_tables_sync():
        # All Table objects that belong to `metadata` will be created
        metadata.create_all(engine)

    # Run the synchronous table creation in FastAPI's thread pool
    await run_in_threadpool(create_tables_sync)
    print("Database tables created/checked.")

    # Optional: Basic connection test (also run in threadpool)
    try:
        def test_connection_sync():
            with SessionLocal() as session:
                result = session.execute(text("SELECT 1")).scalar_one()
                return result
        result = await run_in_threadpool(test_connection_sync)
        print(f"Database connection successful: {result}")
    except Exception as e:
        print(f"Database connection test failed: {e}")
        # In a real application, you might re-raise or log this more robustly
