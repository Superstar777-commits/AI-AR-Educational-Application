"""
    File handles all the common repos and services necessary for the routers
"""

from sqlalchemy.orm import Session # Import Session for synchronous context
from fastapi import Depends
from typing import AsyncGenerator, Any

from src.core.database import get_db # Import your get_db dependency

from src.repositories.user_repository import UserRepository
from src.repositories.question_repository import QuestionRepository
from src.repositories.quiz_repository import QuizRepository
from src.repositories.answer_repository import AnswerRepository
from src.repositories.analysis_repository import AnalysisRepository
from src.repositories.log_repository import LogRepository
from src.repositories.qoptions_repository import QOptionsRepository
from src.repositories.topics_repository import TopicsRepository
from src.repositories.schools_repository import SchoolRepository

# from src.repositories.data_repository import DataRepository # Adjust this if it expects AsyncSession
from src.services.user_service import UserService
from src.services.question_service import QuestionService
from src.services.quiz_service import QuizService
from src.services.answer_service import AnswerService
from src.services.analysis_service import AnalysisService
from src.services.log_service import LogService
from src.services.qoption_service import QOPtionService
from src.services.topic_service import TopicService
from src.services.school_service import SchoolService

# from src.ml_core.model_manager import ModelManager # Adjusted path for clarity
from src.services.ml_service import MLService

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

def get_quiz_repository(db: Session = Depends(get_db_session)) -> QuizRepository:
    return QuizRepository(db)

def get_answer_repository(db: Session = Depends(get_db_session)) -> AnswerRepository:
    return AnswerRepository(db)

def get_analysis_repository(db: Session = Depends(get_db_session)) -> AnalysisRepository:
    return AnalysisRepository(db)

def get_log_repository(db: Session = Depends(get_db_session)) -> LogRepository:
    return LogRepository(db)

def get_topics_repository(db: Session = Depends(get_db_session)) -> TopicsRepository:
    return TopicsRepository(db)

def get_school_repository(db: Session = Depends(get_db_session)) -> SchoolRepository:
    return SchoolRepository(db)

def get_qoptions_repository(db: Session = Depends(get_db_session)) -> QOptionsRepository:
    return QOptionsRepository(db)


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

def get_quiz_service(
        quiz_repo: QuizRepository = Depends(get_quiz_repository)
) -> QuizService:
    return QuizService(quiz_repo)

def get_answer_service(
        answer_repo: AnswerRepository = Depends(get_answer_repository),
        log_repo: LogRepository = Depends(get_log_repository)
) -> AnswerService:
    return AnswerService(answer_repo, log_repo)

def get_analysis_service(
        analysis_repo: AnalysisRepository = Depends(get_analysis_repository)
) -> AnalysisService:
    return AnalysisService(analysis_repo)

def get_log_service(
        log_repo: LogRepository = Depends(get_log_repository)
) -> LogService:
    return LogService(log_repo)
""" def get_model_manager() -> ModelManager:
    return ModelManager() """

def get_qoption_service(
    qopt_repo: QOptionsRepository = Depends(get_qoptions_repository)
) -> QOPtionService:
    return QOPtionService(qopt_repo)

def get_topic_service(
    topic_repo: TopicsRepository = Depends(get_topics_repository)
) -> TopicService:
    return TopicService(topic_repo)

def get_school_service(
    school_repo: SchoolRepository = Depends(get_school_repository)
) -> SchoolService:
    return SchoolService(school_repo)


def get_ml_service(
    analysis_repo: AnalysisRepository = Depends(get_analysis_repository),
    answer_repo: AnswerRepository = Depends(get_answer_repository),
    log_repo: LogRepository = Depends(get_log_repository),
    question_repo: QuestionRepository = Depends(get_question_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    quiz_repo: QuizRepository = Depends(get_quiz_repository)
) -> MLService:
    return MLService(analysis_repo, answer_repo, log_repo, question_repo, user_repo, quiz_repo)
