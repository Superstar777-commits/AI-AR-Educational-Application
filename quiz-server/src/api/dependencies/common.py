from sqlalchemy.orm import Session # Import Session for synchronous context
from fastapi import Depends
from typing import AsyncGenerator, Any

from src.core.database import get_db # Import your get_db dependency

from src.repositories.user_repository import UserRepository
from src.repositories.question_repository import QuestionRepository
# from src.repositories.data_repository import DataRepository # Adjust this if it expects AsyncSession
from src.services.user_service import UserService
from src.services.question_service import QuestionService
# from src.ml_core.model_manager import ModelManager # Adjusted path for clarity
# from src.services.ml_service import MLService

# Database dependency (now yields a synchronous Session)
async def get_db_session() -> AsyncGenerator[Session, Any]: # Correct type hint for async generator
    """Dependency to get a synchronous database session within an async context."""
    async with get_db() as db: # Use async with to enter the async context manager
        yield db

# Repository dependencies - ensure they are correctly typed for the synchronous Session
def get_user_repository(db: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)

def get_question_repository(db: Session = Depends(get_db_session)) -> QuestionRepository:
    return QuestionRepository(db)

""" def get_data_repository(db: Session = Depends(get_db_session)) -> DataRepository:
    # If DataRepository needs a database session, it should also expect Session
    # You'll need to update DataRepository's __init__ and methods similar to UserRepository
    return DataRepository(db) """

# Service dependencies (no change needed as they interact with repositories' async methods)
def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repo)

def get_question_service(
    question_repo: QuestionRepository = Depends(get_question_repository)
) -> QuestionService:
    return QuestionService(question_repo)

""" def get_model_manager() -> ModelManager:
    return ModelManager() """

""" def get_ml_service(
    model_manager: ModelManager = Depends(get_model_manager),
    data_repo: DataRepository = Depends(get_data_repository)
) -> MLService:
    return MLService(model_manager, data_repo) """
