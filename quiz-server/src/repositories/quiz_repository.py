"""
    Repository for Quizzes
    Contains all the concrete implementations for quiz_service functions
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from starlette.concurrency import run_in_threadpool

from ..models.quiz_model import quizzes_table
from ..api.schemas.quiz_schema import QuizCreate, QuizResponse, QuizUpdate

class QuizRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_quiz(self, quiz_data: QuizCreate) -> Dict[str, Any] | None:
        """Creates a new quiz record"""
        def _create_quiz_sync():
            stmt = insert(quizzes_table).values(
                title = quiz_data.title,
                duration = quiz_data.duration
            )

            result = self.db.execute(stmt)
            self.db.commit()

            created_quiz_row = self.db.execute(
                select(quizzes_table).where(quizzes_table.c.id == result.lastrowid)
            ).first()

            return created_quiz_row._asdict() if created_quiz_row else None

        return await run_in_threadpool(_create_quiz_sync)

    async def get_quiz_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a quiz by ID"""
        def _get_quiz_by_id_sync():
            stmt = select(quizzes_table).where(quizzes_table.c.id == id)
            quiz_row = self.db.execute(stmt).first()
            return quiz_row._asdict() if quiz_row else None
        return await run_in_threadpool(_get_quiz_by_id_sync)

    async def get_quizzes(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves a list of quizzes"""
        def _get_quizzes_sync():
            stmt = select(quizzes_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]

        return await run_in_threadpool(_get_quizzes_sync)