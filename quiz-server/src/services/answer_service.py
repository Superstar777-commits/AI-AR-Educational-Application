from typing import Optional, List, Dict, Any
from src.api.schemas.answer_schema import AnswerResponse, AnswerCreate
from src.repositories.answer_repository import AnswerRepository

class AnswerService:
    def __init__(self, answer_repo: AnswerRepository) -> None:
        self.answer_repo = answer_repo

    async def create_answer(self, answer_data: AnswerCreate):
        """
            Creates a new answer
        """
        answer_dict = await self.answer_repo.create_answer(answer_data)
        return answer_dict

    async def get_answer_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
            Retrieves an answer by ID
        """
        answer_dict = await self.answer_repo.get_answer_by_id(id)
        return answer_dict

    async def get_answers_by_user_id(self, id: int, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves answers by user id"""
        answers_list_dict = await self.answer_repo.get_answers_by_user_id(id, skip=skip, limit=limit)
        return answers_list_dict

    async def get_answers(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all answers"""
        answers_list_dict = await self.answer_repo.get_answers(skip=skip, limit=limit)
        return answers_list_dict
