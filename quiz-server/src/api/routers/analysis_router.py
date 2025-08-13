"""
    File handles all the API routes for Analysis table
    
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

# import pydantic schemas, service, dependency
from src.api.schemas.analysis_schema import AnalysisCreate, AnalysisResponse
from src.services.analysis_service import AnalysisService
from src.api.dependencies.common import get_analysis_service

router = APIRouter(prefix="/analyses", tags=["Analyses"])

@router.post("/", response_model=AnalysisCreate, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysis_data: AnalysisCreate,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> AnalysisResponse:
    """Creates a analysis"""
    analysis_dict = await analysis_service.create_analysis(analysis_data)
    print(f"Analysis dict: {analysis_dict}")
    if analysis_dict == None:
        raise HTTPException(status_code=400, detail="Analysis could not be created")
    return AnalysisResponse.model_validate(analysis_dict)

@router.get("/{id}", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def get_analysis_by_id(
    id: int,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> AnalysisResponse:
    """Retrieve an analysis by ID"""
    analysis_dict = await analysis_service.get_analysis_by_id(id)
    print(f"Analysis dict: {analysis_dict}")
    if analysis_dict == None:
        raise HTTPException(status_code=404, detail="Analysis could not be found")
    return AnalysisResponse.model_validate(analysis_dict)

@router.get("/user/{id}", response_model=List[AnalysisResponse], status_code=status.HTTP_200_OK)
async def get_analyses_by_user_id(
    id: int,
    skip: int = 0,
    limit: int = 10,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> List[AnalysisResponse]:
    """Retrieves all analyses for a user"""
    analyses_list_dict = await analysis_service.get_analyses_by_user_id(id=id, skip=skip, limit=limit)
    if analyses_list_dict == None:
        raise HTTPException(status_code=400, detail="Analyses for user could not be found")
    return [AnalysisResponse.model_validate(analysis_dict) for analysis_dict in analyses_list_dict]