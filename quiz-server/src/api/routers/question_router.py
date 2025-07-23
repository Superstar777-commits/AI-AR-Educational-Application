"""
    File handles all the routes for Question table
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from src.api.schemas.question_schema import QuestionCreate, QuestionResponse

from src.services.question_service import QuestionService

from src.api.dependencies.common import get_question_service

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question_route(
    question_data: QuestionCreate,
    question_service: QuestionService = Depends(get_question_service)
) -> QuestionResponse:
    """
    Create a new question, expects QuestionCreate schema as input
    Returns QuestionsResponse schema on success
    """
    question_dict = await question_service.create_question(question_data=question_data)
    print(f"Question dict: {question_dict}")
    if question_dict == None:
        raise HTTPException(status_code=400, detail="Question failed to create")
    return QuestionResponse.model_validate(question_dict)

@router.get("/{id}", response_model=QuestionResponse)
async def get_question_route(
    id: int,
    question_service: QuestionService = Depends(get_question_service)
) -> QuestionResponse:
    """
        Retrieve a question by their ID
    """
    question_dict = await question_service.get_question_by_id(id=id)
    if not question_dict:
        raise HTTPException(status_code=400, detail="Question not found.")
    return QuestionResponse.model_validate(question_dict)

@router.get("/", response_model=List[QuestionResponse])
async def get_all_questions_route(
    skip: int = 0,
    limit: int = 10,
    question_service: QuestionService = Depends(get_question_service)
) -> List[QuestionResponse]:
    """
        Retrieves a list of all questions
    """
    questions_list_dict = await question_service.get_questions(skip=skip, limit=limit)
    return [QuestionResponse.model_validate(question_dict) for question_dict in questions_list_dict]

@router.get("/quiz/{id}", response_model=List[QuestionResponse])
async def get_all_questions_by_quiz_id_route(
    id: int,
    skip: int = 0,
    limit: int = 10,
    question_service: QuestionService = Depends(get_question_service)
) -> List[QuestionResponse]:
    """
        Retrieves a list of all questions
    """
    questions_list_dict = await question_service.get_questions_by_quiz_id(id=id, skip=skip, limit=limit)
    return [QuestionResponse.model_validate(question_dict) for question_dict in questions_list_dict]