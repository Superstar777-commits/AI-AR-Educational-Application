"""
    Repository for Logs
    Contains all the concrete implementations for log_service functions
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, Select
from starlette.concurrency import run_in_threadpool

from ..models.logs_model import logs_table
from ..models.question_model import questions_table
from ..api.schemas.log_schema import LogCreate, LogUpdate

class LogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def create_log(self, log_data: LogCreate):
        """Creates a new log record"""
        def _create_log_sync():
            stmt = insert(logs_table).values(
                action = log_data.action,
                time = log_data.time,
                user_id = log_data.user_id,
                question_id = log_data.question_id
            )

            result = self.db.execute(stmt)
            self.db.commit()

            created_log_row = self.db.execute(
                select(logs_table).where(logs_table.c.id == result.lastrowid)
            ).first()

            return created_log_row._asdict() if created_log_row else None
        return await run_in_threadpool(_create_log_sync)

    async def get_log_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a log by its id"""
        def _get_log_by_sync():
            stmt = select(logs_table).where(logs_table.c.id == id)
            log_row = self.db.execute(stmt).first()
            return log_row._asdict() if log_row else None
        return await run_in_threadpool(_get_log_by_sync)

    async def get_logs_by_user_id(self, id: int, question_id: Optional[int] = None, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all user logs"""
        def _get_logs_by_user_id_sync():
            stmt: Select[Any]
            print(f"question_id: {question_id}")
            if question_id is not None:
                stmt = select(logs_table, questions_table.c.question).where((logs_table.c.user_id == id) & (logs_table.c.question_id == question_id)).offset(skip).limit(limit)
            else:
                stmt = select(logs_table, questions_table.c.question).where(logs_table.c.user_id == id).offset(skip).limit(limit)
            print(f"stmt: {stmt}")
            results = self.db.execute(stmt).fetchall()
            print(f"results: {results}")
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_logs_by_user_id_sync)

    async def get_logs(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all logs"""
        def _get_logs_sync():
            stmt = select(logs_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_logs_sync)

    async def update_log(self, id: int, log_data: LogUpdate) -> Dict[str, Any] | None:
        """
            Updates a log's information
            Return:
                Dict[str, Any]: The updated row
                None: Return null if no row updated
        """
        def _update_log_sync():
            # create a dict of non-None values from log data
            update_values = {k: v for k, v in log_data.model_dump(exclude_unset=True).items() if v is not None}

            if not update_values:
                log_row = self.db.execute(select(logs_table).where(logs_table.c.id == id)).first()
                return log_row._asdict() if log_row else None

            stmt = update(logs_table).where(logs_table.c.id == id).values(**update_values)
            self.db.execute(stmt)
            self.db.commit()

            # fetch the updated log to return its current data
            updated_log_row = self.db.execute(
                select(logs_table).where(logs_table.c.id == id)
            ).first()
            return updated_log_row._asdict() if updated_log_row else None

        return await run_in_threadpool(_update_log_sync)