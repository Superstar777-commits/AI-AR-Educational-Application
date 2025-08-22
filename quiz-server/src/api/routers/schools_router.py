from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.api.schemas.schools_schema import SchoolCreate, SchoolResponse, SchoolUpdate

from src.services.school_service import SchoolService

from src.api.dependencies.common import get_school_service

router = APIRouter(prefix="/schools", tags=["Schools"])

@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def create_school_route(
    school_data: SchoolCreate,
    school_service: SchoolService = Depends(get_school_service)
) -> SchoolResponse:
    """Create a new school"""
    school_dict = await school_service.create_school(school_data)
    if school_dict == None:
        raise HTTPException(status_code=400, detail="Could not create school")
    return SchoolResponse.model_validate(school_dict)

@router.get("/all", response_model=List[SchoolResponse])
async def get_all_schools(
    skip: int = 0,
    limit: int = 10,
    school_service: SchoolService = Depends(get_school_service)
) -> List[SchoolResponse]:
    """Retrieve all schools"""
    school_list_dict = await school_service.get_schools(skip, limit)
    return [SchoolResponse.model_validate(school_dict) for school_dict in school_list_dict]

@router.get("/{id}", response_model=SchoolResponse)
async def get_school(
    id: int,
    school_service: SchoolService = Depends(get_school_service)
) -> SchoolResponse:
    """Retrieve a school by its ID"""
    school_dict = await school_service.get_school(id)
    if school_dict == None:
        raise HTTPException(status_code=404, detail="School not found")
    return SchoolResponse.model_validate(school_dict)

@router.put("/{id}", response_model=SchoolResponse)
async def update_school(
    id: int,
    school_data: SchoolUpdate,
    school_service: SchoolService = Depends(get_school_service)
) -> SchoolResponse:
    """Update a school by its ID"""
    school_dict = await school_service.update_school(id, school_data)
    if school_dict == None:
        raise HTTPException(status_code=404, detail="School not found or could not be updated")
    return SchoolResponse.model_validate(school_dict)


