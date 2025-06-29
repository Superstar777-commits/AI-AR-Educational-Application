from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from starlette.concurrency import run_in_threadpool

from ..models.question_model import questions_table
from ..api.schemas.question_schema import QuestionCreate, QuestionUpdate, MarkAsDone

class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_question(self, question_data: QuestionCreate) -> Dict[str, Any] | None:
        """
        Creates a new question record
        """
        def _create_question_sync():
            stmt = insert(questions_table).values(
                question = question_data.question,
                marks = question_data.marks,
                level = question_data.level,
                correctAnswer = question_data.correctAnswer,
                quiz_id = question_data.quiz_id
            )

            result = self.db.execute(stmt)
            self.db.commit()

            created_question_row = self.db.execute(
                select(questions_table).where(questions_table.c.id == result.lastrowid)
            ).first()

            return created_question_row._asdict() if created_question_row else None
        return await run_in_threadpool(_create_question_sync)

    async def get_question_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
            Retrieves a question by ID
            Returns the question
        """
        def _get_question_by_id_sync():
            stmt = select(questions_table).where(questions_table.c.id == id)
            question_row = self.db.execute(stmt).first()
            return question_row._asdict() if question_row else None
        return await run_in_threadpool(_get_question_by_id_sync)

    async def get_questions_by_quiz_id(self, id: int, skip: int=0, limit:int=10) -> List[Dict[str, Any]]:
        """Retrieves questions by their quiz id foreign key"""
        def _get_questions_by_quiz_id_sync():
            stmt = select(questions_table).where(questions_table.c.quiz_id == id).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_questions_by_quiz_id_sync)

    async def get_questions(self, skip: int=0, limit:int=10) -> List[Dict[str, Any]]:
        """Retrieves a list of questions"""
        def _get_questions_sync():
            stmt = select(questions_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]

        return await run_in_threadpool(_get_questions_sync)
