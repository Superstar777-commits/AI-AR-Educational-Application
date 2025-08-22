from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from starlette.concurrency import run_in_threadpool

from ..models.topics_model import topics_table
from ..api.schemas.topics_schema import TopicCreate, TopicUpdate

class TopicsRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_topic(self, topic_data: TopicCreate):
        def _create_topic_sync():
            stmt = insert(topics_table).values(
                name = topic_data.name,
                details = topic_data.details
            )

            result = self.db.execute(stmt)
            self.db.commit()

            created_log_row = self.db.execute(
                select(topics_table).where(topics_table.c.id == result.lastrowid)
            ).first()

            return created_log_row._asdict() if created_log_row else None
        return await run_in_threadpool(_create_topic_sync)

    async def get_topic(self, id: int) -> Dict[str, Any] | None:
        def _get_topic_sync():
            stmt = select(topics_table).where(topics_table.c.id == id)
            topic_row = self.db.execute(stmt).first()
            return topic_row._asdict() if topic_row else None
        return await run_in_threadpool(_get_topic_sync)

    async def get_all_topics(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        def _get_all_topics_sync():
            stmt = select(topics_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]
        return await run_in_threadpool(_get_all_topics_sync)

    async def update_topic(self, id: int, topic_data: TopicUpdate) -> Dict[str, Any] | None:
        def _update_topic_sync():
            update_values = {k: v for k, v in topic_data.model_dump(exclude_unset=True).items() if v is not None}

            if not update_values:
                top_row = self.db.execute(select(topics_table).where(topics_table.c.id == id)).first()
                return top_row._asdict() if top_row else None

            stmt = update(topics_table).where(topics_table.c.id == id).values(**update_values)
            self.db.execute(stmt)
            self.db.commit()

            updated_topic_row = self.db.execute(
                select(topics_table).where(topics_table.c.id == id)
            ).first()
            return updated_topic_row._asdict() if updated_topic_row else None
        return await run_in_threadpool(_update_topic_sync)