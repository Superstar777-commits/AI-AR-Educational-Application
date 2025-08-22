from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from starlette.concurrency import run_in_threadpool

from ..models.schools_model import schools_table
from ..api.schemas.schools_schema import SchoolCreate, SchoolUpdate

class SchoolRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_school(self, school_data: SchoolCreate) -> Dict[str, Any] | None:
        def _create_school_sync():
            stmt = insert(schools_table).values(
                name = school_data.name,
                province = school_data.province,
                area = school_data.area,
                type = school_data.type
            )

            result = self.db.execute(stmt)
            self.db.commit()

            row = self.db.execute(
                select(schools_table).where(schools_table.c.id == result.lastrowid)
            ).first()

            return row._asdict() if row else None
        return await run_in_threadpool(_create_school_sync)

    async def get_schools(self, skip: int=0, limit=100) -> List[Dict[str, Any]]:
        def _get_schools_sync():
            stmt = select(schools_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_schools_sync)

    async def get_school_by_id(self, id: int) -> Dict[str, Any] | None:
        def _get_school_by_id_sync():
            stmt = select(schools_table).where(schools_table.c.id == id)
            school_row = self.db.execute(stmt).first()
            return school_row._asdict() if school_row else None
        return await run_in_threadpool(_get_school_by_id_sync)

    async def update_school(self, id: int, school_data: SchoolUpdate) -> Dict[str, Any] | None:
        def _update_school_sync():
            update_values = {k: v for k, v in school_data.model_dump(exclude_unset=True).items() if v is not None}

            if not update_values:
                school_row = self.db.execute(select(schools_table).where(schools_table.c.id == id)).first()
                return school_row._asdict() if school_row else None

            stmt = update(schools_table).where(schools_table.c.id == id).values(**update_values)
            self.db.execute(stmt)
            self.db.commit()

            updated_row = self.db.execute(
                select(schools_table).where(schools_table.c.id == id)
            ).first()

            return updated_row._asdict() if updated_row else None

        return await run_in_threadpool(_update_school_sync)