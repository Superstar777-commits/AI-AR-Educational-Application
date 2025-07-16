from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from starlette.concurrency import run_in_threadpool

from ..models.answers_model import answers_table
from ..api.schemas.answer_schema import AnswerCreate

class AnswerRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_answer(self, answer_data: AnswerCreate):
        """
        Creates a new answer record
        """

        def _create_answer_sync():
            stmt = insert(answers_table).values(
                question_id = answer_data.question_id,
                user_id = answer_data.user_id,
                answer = answer_data.answer
            )

            result = self.db.execute(stmt)
            self.db.commit()

            created_answer_row = self.db.execute(
                select(answers_table).where(answers_table.c.id == result.lastrowid)
            ).first()

            return created_answer_row._asdict() if created_answer_row else None
        return await run_in_threadpool(_create_answer_sync)

    async def get_answer_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
            Retrieves an answer by ID
        """

        def _get_answer_by_id_sync():
            stmt = select(answers_table).where(answers_table.c.id == id)
            answer_row = self.db.execute(stmt).first()
            return answer_row._asdict() if answer_row else None
        return await run_in_threadpool(_get_answer_by_id_sync)

    async def get_answers_by_user_id(self, id: int, skip: int = 0, limit: int=10) -> List[Dict[str, Any]]:
        """
        Retrieves answers by user id
        """
        def _get_answers_by_user_id_sync():
            stmt = select(answers_table).where(answers_table.c.user_id == id).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_answers_by_user_id_sync)

    async def get_answers(self, skip: int = 0, limit = 10) -> List[Dict[str, Any]]:
        """Retrieves all answers"""
        def _get_answers_sync():
            stmt = select(answers_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_answers_sync)