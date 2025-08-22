from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from src.api.schemas.qoptions_schema import QOptionsCreate, QOptionsResponse, QOptionsUpdate
from src.services.qoption_service import QOPtionService

from src.api.dependencies.common import get_qoption_service

router = APIRouter(prefix="/qoptions", tags=["QOptions"])

@router.post("/", response_model=QOptionsResponse, status_code=status.HTTP_201_CREATED)
async def create_qoption_route(
    qoption_data: QOptionsCreate,
    qoption_service: QOPtionService = Depends(get_qoption_service)
) -> QOptionsResponse:
    """Create a new question option"""
    qoption_dict = await qoption_service.create_qopt(qoption_data)
    if qoption_dict == None:
        raise HTTPException(status_code=400, detail="Could not create question option")
    return QOptionsResponse.model_validate(qoption_dict)

@router.get("/all/{q_id}", response_model=List[QOptionsResponse])
async def get_all_qoptions(
    q_id: int,
    skip: int = 0,
    limit: int = 10,
    qoption_service: QOPtionService = Depends(get_qoption_service)
) -> List[QOptionsResponse]:
    """Retrieve all question options"""
    qoption_list_dict = await qoption_service.get_qopts_by_question(q_id, skip, limit)
    return [QOptionsResponse.model_validate(qoption_dict) for qoption_dict in qoption_list_dict]

@router.get("/{id}", response_model=QOptionsResponse)
async def get_qoption(
    id: int,
    qoption_service: QOPtionService = Depends(get_qoption_service)
) -> QOptionsResponse:
    """Retrieve a question option by its ID"""
    qoption_dict = await qoption_service.get_qopt(id)
    if qoption_dict == None:
        raise HTTPException(status_code=404, detail="Question option not found")
    return QOptionsResponse.model_validate(qoption_dict)

@router.put("/{id}", response_model=QOptionsResponse)
async def update_qoption(
    id: int,
    qoption_data: QOptionsUpdate,
    qoption_service: QOPtionService = Depends(get_qoption_service)
) -> QOptionsResponse:
    """Update a question option by its ID"""
    qoption_dict = await qoption_service.update_qopt(id, qoption_data)
    if qoption_dict == None:
        raise HTTPException(status_code=404, detail="Question option not found or could not be updated")
    return QOptionsResponse.model_validate(qoption_dict)