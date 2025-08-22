from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.api.schemas.topics_schema import TopicCreate, TopicResponse, TopicUpdate
from src.services.topic_service import TopicService

from src.api.dependencies.common import get_topic_service

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic_route(
    topic_data: TopicCreate,
    topic_service: TopicService = Depends(get_topic_service)
) -> TopicResponse:
    """Create a new topic"""
    topic_dict = await topic_service.create_topic(topic_data)
    if topic_dict == None:
        raise HTTPException(status_code=400, detail="Could not create topic")
    return TopicResponse.model_validate(topic_dict)

@router.get("/all", response_model=List[TopicResponse])
async def get_all_topics(
    skip: int = 0,
    limit: int = 10,
    topic_service: TopicService = Depends(get_topic_service)
) -> List[TopicResponse]:
    """Retrieve all topics"""
    topic_list_dict = await topic_service.get_all_topics(skip, limit)
    return [TopicResponse.model_validate(topic_dict) for topic_dict in topic_list_dict]

@router.get("/{id}", response_model=TopicResponse)
async def get_topic(
    id: int,
    topic_service: TopicService = Depends(get_topic_service)
) -> TopicResponse:
    """Retrieve a topic by its ID"""
    topic_dict = await topic_service.get_topic(id)
    if topic_dict == None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return TopicResponse.model_validate(topic_dict)

@router.put("/{id}", response_model=TopicResponse)
async def update_topic(
    id: int,
    topic_data: TopicUpdate,
    topic_service: TopicService = Depends(get_topic_service)
) -> TopicResponse:
    """Update a topic by its ID"""
    topic_dict = await topic_service.update_topic(id, topic_data)
    if topic_dict == None:
        raise HTTPException(status_code=404, detail="Topic not found or could not be updated")
    return TopicResponse.model_validate(topic_dict)
