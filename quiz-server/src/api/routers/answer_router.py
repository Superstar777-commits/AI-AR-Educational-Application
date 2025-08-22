"""
    File handles all the routes for Answers table
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

# import pydantic schemes
from src.api.schemas.answer_schema import AnswerCreate, AnswerResponse, AnswerUpdate
from src.api.schemas.log_schema import LogCreate
# import AnswerService
from src.services.answer_service import AnswerService
#import dependency to inject the AnswerService
from src.api.dependencies.common import get_answer_service

router = APIRouter(prefix="/answers", tags=["Answers"])

@router.post("/", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
async def create_answer_route(
    answer_data: AnswerCreate,
    log_data: LogCreate,
    answer_service: AnswerService = Depends(get_answer_service)
) -> AnswerResponse:
    """Create a new answer
        User sends their answer to a question
    """
    answer_dict = await answer_service.create_answer(answer_data, log_data)
    print(f"Answer dict: {answer_dict}")
    if answer_dict == None:
        raise HTTPException(status_code=400, detail="Could not send answer")
    return AnswerResponse.model_validate(answer_dict)

@router.get("/all", response_model=List[AnswerResponse])
async def get_all_answers(
    skip: int = 0,
    limit: int = 10,
    answer_service: AnswerService = Depends(get_answer_service)
) -> List[AnswerResponse]:
    """Retrieve all answers"""
    answer_list_dict = await answer_service.get_answers(skip, limit)
    return [AnswerResponse.model_validate(answer_dict) for answer_dict in answer_list_dict]

@router.get("/user/{id}", response_model=List[AnswerResponse])
async def get_all_answers_by_user(
    id: int,
    skip: int = 0,
    limit: int = 10,
    answer_service: AnswerService = Depends(get_answer_service)
) -> List[AnswerResponse]:
    """Retrieves all answers by users"""
    answers_list_dict = await answer_service.get_answers_by_user_id(id=id, skip=skip, limit=limit)
    return [AnswerResponse.model_validate(answer_dict) for answer_dict in answers_list_dict]

@router.get("/user/{user_id}/quiz/{quiz_id}", response_model=List[AnswerResponse])
async def get_all_answers_by_user_and_quiz_id(
    user_id: int,
    quiz_id: int,
    skip: int = 0,
    limit: int = 10,
    answer_service: AnswerService = Depends(get_answer_service)
) -> List[AnswerResponse]:
    """Retrieves all answers by users"""
    answers_list_dict = await answer_service.get_answers_by_user_id_and_quiz_id(user_id=user_id, quiz_id=quiz_id, skip=skip, limit=limit)
    return [AnswerResponse.model_validate(answer_dict) for answer_dict in answers_list_dict]

@router.get("/quiz/{id}", response_model=List[AnswerResponse])
async def get_all_answers_by_quiz_id(
    id: int,
    skip: int = 0,
    limit: int = 10,
    answer_service: AnswerService = Depends(get_answer_service)
) -> List[AnswerResponse]:
    """Retrieves all answers by quiz id"""
    answer_list_dict = await answer_service.get_answers_by_quiz_id(id=id, skip=skip, limit=limit)
    return [AnswerResponse.model_validate(answer_dict) for answer_dict in answer_list_dict]

@router.get("/{id}", response_model=AnswerResponse)
async def get_answer_by_id(
    id: int,
    answer_service: AnswerService = Depends(get_answer_service)
) -> AnswerResponse:
    """Retrieves an answer by id"""
    answer_dict = await answer_service.get_answer_by_id(id)
    return AnswerResponse.model_validate(answer_dict)

@router.patch("/allocate/{id}/{marks}", response_model=AnswerResponse)
async def allocate_marks_to_question(
    id: int,
    marks: int,
    answer_service: AnswerService = Depends(get_answer_service)
) -> AnswerResponse:
    """Allocates marks to a user's answer record"""
    answer_dict = await answer_service.allocate_marks_to_answer(id, marks)
    return AnswerResponse.model_validate(answer_dict)

