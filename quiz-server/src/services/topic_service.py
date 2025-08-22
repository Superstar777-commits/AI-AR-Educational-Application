from typing import Optional, List, Dict, Any
from src.api.schemas.topics_schema import TopicCreate, TopicUpdate

from src.repositories.topics_repository import TopicsRepository

class TopicService:
    def __init__(self, topic_repo: TopicsRepository) -> None:
        self.topic_repo = topic_repo

    async def create_topic(self, topic_data: TopicCreate):
        topic_dict = await self.topic_repo.create_topic(topic_data=topic_data)
        return topic_dict

    async def get_topic(self, id: int) -> Optional[Dict[str, Any]]:
        topic_dict = await self.topic_repo.get_topic(id)
        return topic_dict

    async def get_all_topics(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        topics = await self.topic_repo.get_all_topics(skip, limit)
        return topics

    async def update_topic(self, id: int, topic_data: TopicUpdate) -> Optional[Dict[str, Any]]:
        topic_dict = await self.topic_repo.update_topic(id, topic_data)
        return topic_dict
