"""
    Repository for QOptions
    Contains all the concrete implementations for qoptions_service functions
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, Select
from starlette.concurrency import run_in_threadpool

from ..models.qoptions_model import qoptions_table
from ..models.question_model import questions_table
from ..api.schemas.qoptions_schema import QOptionsCreate, QOptionsUpdate

class QOptionsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def create_qoption(self, qopt_data: QOptionsCreate):
        """
            Creates a new a question option (qoption)
        """
        def _create_qoption_sync():
            stmt = insert(qoptions_table).values(
                option = qopt_data.option,
                question_id = qopt_data.question_id
            )

            result = self.db.execute(stmt)
            self.db.commit()

            created_qopt_row = self.db.execute(
                select(qoptions_table).where(qoptions_table.c.id == result.lastrowid)
            ).first()

            return created_qopt_row._asdict() if created_qopt_row else None
        return await run_in_threadpool(_create_qoption_sync)

    async def get_qoption_by_id(self, id: int) -> Dict[str, Any] | None:
        """
            Retrieves a question option by its ID
        """
        def _get_qopt_by_id_sync():
            stmt = select(qoptions_table).where(qoptions_table.c.id == id)
            qopt_row = self.db.execute(stmt).first()
            return qopt_row._asdict() if qopt_row else None
        return await run_in_threadpool(_get_qopt_by_id_sync)

    async def get_qoptions_by_question(self, q_id: int, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """
            Retrieves question options for a question
            i.e. if a quesiton is a multiple choice, then it will fetch all those options related to the question
        """
        def _get_qopts_by_q_sync():
            stmt = select(qoptions_table).where(qoptions_table.c.question_id == q_id).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_qopts_by_q_sync)

    async def update_qopt(self, id: int, qopt_data: QOptionsUpdate):
        def _update_qopt_sync():
            update_values = {k: v for k, v in qopt_data.model_dump(exclude_unset=True).items()}

            if not update_values:
                qopt_row = self.db.execute(select(qoptions_table).where(qoptions_table.c.id == id)).first()
                return qopt_row._asdict() if qopt_row else None

            stmt = update(qoptions_table).where(qoptions_table.c.id == id).values(**update_values)

            self.db.execute(stmt)
            self.db.commit()

            updated_qopt_row = self.db.execute(
                select(qoptions_table).where(qoptions_table.c.id == id)
            ).first()

            return updated_qopt_row._asdict() if updated_qopt_row else None
        return run_in_threadpool(_update_qopt_sync)
