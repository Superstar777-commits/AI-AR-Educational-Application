"""
    Repository for Logs
    Contains all the concrete implementations for log_service functions
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from starlette.concurrency import run_in_threadpool

from ..models.logs_model import logs_table
from ..api.schemas.log_schema import LogCreate

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

    async def get_logs_by_user_id(self, id: int, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all user logs"""
        def _get_logs_by_user_id_sync():
            stmt = select(logs_table).where(logs_table.c.user_id == id).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_logs_by_user_id_sync)

    async def get_logs(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all logs"""
        def _get_logs_sync():
            stmt = select(logs_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_logs_sync)

