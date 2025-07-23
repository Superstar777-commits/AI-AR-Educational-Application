"""
    File handles all the routes for Quiz router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from src.api.schemas.quiz_schema import QuizCreate, QuizResponse, QuizUpdate
from src.services.quiz_service import QuizService
from src.api.dependencies.common import get_quiz_service

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz_route(
    quiz_data: QuizCreate,
    quiz_service: QuizService = Depends(get_quiz_service)
) -> QuizResponse:
    """Create a new quiz"""
    quiz_dict = await quiz_service.create_quiz(quiz_data)
    print(f"Quiz dict: {quiz_dict}")
    if quiz_dict == None:
        raise HTTPException(status_code=400, detail="Quiz was not created")
    return QuizResponse.model_validate(quiz_dict)

@router.get("/{id}", response_model=QuizResponse, status_code=status.HTTP_200_OK)
async def get_quiz_by_id(
    id: int,
    quiz_service: QuizService = Depends(get_quiz_service)
) -> QuizResponse:
    """Retrieves a quiz by ID"""
    quiz_dict = await quiz_service.get_quiz_by_id(id)
    if not quiz_dict:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return QuizResponse.model_validate(quiz_dict)

@router.get("/", response_model=List[QuizResponse])
async def get_all_quizzes_route(
        skip: int = 0,
        limit: int = 10,
        quiz_service: QuizService = Depends(get_quiz_service)
) -> List[QuizResponse]:
    """Retrieve list of all quizzes"""
    quiz_list_dict = await quiz_service.get_quizzes(skip=skip, limit=limit)
    return [QuizResponse.model_validate(quiz_dict) for quiz_dict in quiz_list_dict]
