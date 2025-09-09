"""
    Repository for Answers
    Contains all the concrete implementations for answer_service functions
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from starlette.concurrency import run_in_threadpool

from ..models.answers_model import answers_table
from ..models.question_model import questions_table
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
                quiz_id = answer_data.quiz_id,
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
            stmt = select(answers_table, questions_table.c.question).where(answers_table.c.user_id == id).join(questions_table, answers_table.c.question_id == questions_table.c.id).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_answers_by_user_id_sync)

    async def get_answers_by_user_and_quiz_id(self, user_id: int, quiz_id: int, skip: int = 0, limit: int=10) -> List[Dict[str, Any]]:
        """
        Retrieves answers by user id
        """
        def _get_answers_by_user_id_sync():
            stmt = select(
                    answers_table.c.question_id,
                    answers_table.c.user_id,
                    answers_table.c.quiz_id,
                    answers_table.c.answer,
                    answers_table.c.marksAchieved.label('marks_achieved'),
                    questions_table.c.question,
                    questions_table.c.correctAnswer,
                    questions_table.c.marks.label('total_marks')
                ).where(
                    (answers_table.c.user_id == user_id) & (answers_table.c.quiz_id == quiz_id)
                ).join(
                    questions_table,
                    answers_table.c.question_id == questions_table.c.id
                ).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_answers_by_user_id_sync)

    async def get_answers_by_quiz_id(self, id:int, skip: int = 0, limit: int=10) -> List[Dict[str, Any]]:
        """
            Retrieves answers through the quiz_id
        """
        def _get_answers_by_quiz_id_sync():
            stmt = select(answers_table, questions_table.c.question).where(answers_table.c.quiz_id == id).join(questions_table, answers_table.c.question_id == questions_table.c.id).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_answers_by_quiz_id_sync)

    async def get_answers(self, skip: int = 0, limit = 10) -> List[Dict[str, Any]]:
        """Retrieves all answers"""
        def _get_answers_sync():
            stmt = select(answers_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_answers_sync)

    async def get_answers_with_questions(self, skip: int = 0, limit = 10) -> List[Dict[str, Any]]:
        """Retrieves all answers"""
        def _get_answers_sync():
            stmt = select(
                    answers_table.c.id,
                    answers_table.c.question_id,
                    answers_table.c.user_id,
                    answers_table.c.quiz_id,
                    answers_table.c.answer,
                    questions_table.c.marks,
                    answers_table.c.marksAchieved,
                    questions_table.c.question,
                    questions_table.c.correctAnswer,
                    questions_table.c.type
                ).join(
                    questions_table,
                    answers_table.c.question_id == questions_table.c.id
                ).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_answers_sync)

    async def allocate_marks_to_answer(self, id: int, marks: int) -> Optional[Dict[str, Any]]:
        """Allocate marks to a user's answer (basically updating their record)"""
        def _allocate_marks_to_answer():
            stmt = update(answers_table).where(answers_table.c.id == id).values(marksAchieved = marks)
            result = self.db.execute(stmt)
            self.db.commit()
            answer_row = self.db.execute(
                select(answers_table).where(answers_table.c.id == result.lastrowid)
            ).first()
            return answer_row._asdict() if answer_row else None
        return await run_in_threadpool(_allocate_marks_to_answer)

