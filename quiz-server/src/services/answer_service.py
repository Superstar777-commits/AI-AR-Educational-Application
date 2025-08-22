"""
    Service for Answers
    Contains all the logic for the answer_router
"""

from typing import Optional, List, Dict, Any
from src.api.schemas.answer_schema import AnswerResponse, AnswerCreate
from src.api.schemas.log_schema import LogCreate
from src.repositories.answer_repository import AnswerRepository
from src.repositories.log_repository import LogRepository

class AnswerService:
    def __init__(self, answer_repo: AnswerRepository, log_repo: LogRepository) -> None:
        self.answer_repo = answer_repo
        self.log_repo = log_repo

    async def create_answer(self, answer_data: AnswerCreate, log_data: LogCreate):
        """
            Creates a new answer and adds it log
        """
        answer_dict = await self.answer_repo.create_answer(answer_data)
        await self.log_repo.create_log(log_data)

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

    async def get_answers_by_user_id_and_quiz_id(self, user_id: int, quiz_id: int, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves answers by user id"""
        answers_list_dict = await self.answer_repo.get_answers_by_user_and_quiz_id(user_id=user_id, quiz_id=quiz_id, skip=skip, limit=limit)
        return answers_list_dict

    async def get_answers_by_quiz_id(self, id:int, skip: int = 0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves answers by quiz id"""
        answers_list_dict = await self.answer_repo.get_answers_by_quiz_id(id=id, skip=skip, limit=limit)
        return answers_list_dict

    async def get_answers(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all answers"""
        answers_list_dict = await self.answer_repo.get_answers(skip=skip, limit=limit)
        return answers_list_dict

    async def allocate_marks_to_answer(self, id: int, marks: int) -> Optional[Dict[str, Any]]:
        """Allocates marks to a user's answer"""
        answer_dict = await self.answer_repo.allocate_marks_to_answer(id, marks)
        return answer_dict
