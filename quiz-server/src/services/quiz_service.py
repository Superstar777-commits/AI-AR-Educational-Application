"""
    Service for Quizzes
    Contains all the logic for the quiz_router
"""

from typing import Optional, List, Dict, Any

from src.api.schemas.quiz_schema import QuizCreate, QuizResponse, QuizUpdate

from src.repositories.quiz_repository import QuizRepository

class QuizService:
    def __init__(self, quiz_repo: QuizRepository):
        self.quiz_repo = quiz_repo

    async def create_quiz(self, quiz_data: QuizCreate) -> Optional[Dict[str, Any]]:
        """Creates a new quiz"""
        quiz_dict = await self.quiz_repo.create_quiz(quiz_data)
        return quiz_dict

    async def get_quiz_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a quiz by its ID"""
        quiz_dict = await self.quiz_repo.get_quiz_by_id(id)
        return quiz_dict

    async def get_quizzes(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves a list of quizzes"""
        quiz_list_dict = await self.quiz_repo.get_quizzes(skip=skip, limit=limit)
        return quiz_list_dict