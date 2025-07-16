from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from starlette.concurrency import run_in_threadpool

from ..models.analyses_model import analyses_table
from ..api.schemas.analysis_schema import AnalysisCreate

class AnalysisRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def create_analysis(self, analysis_data: AnalysisCreate):
        """Creates a new analysis record"""
        def _create_analysis_sync():
            stmt = insert(analyses_table).values(
                user_id = analysis_data.user_id,
                question_id = analysis_data.question_id,
                analysis = analysis_data.analysis
            )

            result = self.db.execute(stmt)
            self.db.commit()

            created_analysis_row = self.db.execute(
                select(analyses_table).where(analyses_table.c.id == result.lastrowid)
            ).first()

            return created_analysis_row._asdict() if created_analysis_row else None
        return await run_in_threadpool(_create_analysis_sync)

    async def get_analysis_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Retrieves an analysis by id"""
        def _get_analysis_by_id_sync():
            stmt = select(analyses_table).where(analyses_table.c.id == id)
            analysis_row = self.db.execute(stmt).first()
            return analysis_row._asdict() if analysis_row else None
        return await run_in_threadpool(_get_analysis_by_id_sync)

    async def get_analyses_by_user_id(self, id: int, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all analyses for a user"""
        def _get_analyses_by_user_id_sync():
            stmt = select(analyses_table).where(analyses_table.c.user_id == id).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_analyses_by_user_id_sync)