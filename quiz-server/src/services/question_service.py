"""
    Service for Questions
    Contains all the logic for the question_router
"""

from typing import Optional, List, Dict, Any
from src.api.schemas.question_schema import QuestionCreate, QuestionResponse, QuestionUpdate
from src.repositories.question_repository import QuestionRepository

class QuestionService:
    def __init__(self, question_repo: QuestionRepository) -> None:
        self.question_repo = question_repo

    async def create_question(self, question_data: QuestionCreate) -> Optional[Dict[str, Any]]:
        """
            Creates a new question
        """
        # call the repo to create the question
        # the repo now returns a dict (or None)
        question_dict = await self.question_repo.create_question(question_data)
        return question_dict

    async def get_question_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a question by ID
        returns a dict representation of the user or None if dound
        """
        question_dict = await self.question_repo.get_question_by_id(id)
        return question_dict

    async def get_questions_by_quiz_id(self, id: int, skip: int=0, limit:int=10) -> List[Dict[str, Any]]:
        """Retrieves all questions by quiz id with pagination"""
        questions_list_dict = await self.question_repo.get_questions_by_quiz_id(id=id, skip=skip, limit=limit)
        return questions_list_dict

    async def get_questions(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves all questions through pagination"""
        questions_list_dict = await self.question_repo.get_questions(skip=skip, limit=limit)
        return questions_list_dict