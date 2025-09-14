"""
    Handles DB connections and creating the tables (models)
"""
from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from .config import settings

# The DATABASE_URL is defined in your .env and loaded via config.py
# Make sure your URL uses an async dialect, like 'mysql+asyncmy'
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the asynchronous engine
# pool_pre_ping=True helps maintain connections for long-running apps
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# Create an asynchronous sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# MetaData object to hold Table definitions
metadata = MetaData()

# --- Dependency to get an asynchronous database session ---
@asynccontextmanager
async def get_db():
    """Dependency to get an asynchronous database session.
    It yields the session and ensures it's closed correctly.
    """
    async with AsyncSessionLocal() as session:
        yield session

# --- IMPORTANT: Initialize DB (create tables) during startup ---
async def init_db():
    """Initializes the database: creates tables if they don't exist.
    This runs blocking SQLAlchemy Core operations (create_all) in an async context.
    """
    print("Attempting to initialize database tables (SQLAlchemy Core)...")

    async with async_engine.begin() as conn:
        # run_sync is the correct method to run a synchronous operation in an async context
        await conn.run_sync(metadata.create_all)

    print("Database tables created/checked.")

    # Optional: Basic connection test
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            # The result is now an async Result, so we need to fetch the one value
            scalar_result = result.scalar_one()
            print(f"Database connection successful: {scalar_result}")
    except Exception as e:
        print(f"Database connection test failed: {e}")
