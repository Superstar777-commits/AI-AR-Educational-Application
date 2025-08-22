"""
    File handles all the routes for Logs table
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional

# import Pydantic schemas
from src.api.schemas.log_schema import LogCreate, LogResponse
from src.services.log_service import LogService
from src.api.dependencies.common import get_log_service

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def create_log_route(
    log_data: LogCreate,
    log_service: LogService = Depends(get_log_service)
) -> LogResponse:
    """Creates a new log"""
    log_dict = await log_service.create_log(log_data=log_data)
    print(f"Log dict: {log_dict}")
    if log_dict == None:
        raise HTTPException(status_code=400, detail="Log failed to be created")
    return LogResponse.model_validate(log_dict)

@router.get("/all", response_model=List[LogResponse], status_code=status.HTTP_200_OK)
async def get_all_logs(
    skip: int = 0,
    limit: int = 10,
    log_service: LogService = Depends(get_log_service)
) -> List[LogResponse]:
    """Retrieves all logs"""
    log_list_dict = await log_service.get_logs(skip, limit)
    if log_list_dict == None:
        raise HTTPException(status_code=400, detail="No logs found")
    return [LogResponse.model_validate(log_dict) for log_dict in log_list_dict]

@router.get("/{id}", response_model=LogResponse, status_code=status.HTTP_200_OK)
async def get_log_by_id(
    id: int,
    log_service: LogService = Depends(get_log_service)
) -> LogResponse:
    """Retrieves a log by its ID"""
    log_dict = await log_service.get_log_by_id(id)
    print(f"Log dict: {log_dict}")
    if log_dict == None:
        raise HTTPException(status_code=404, detail="No log found")
    return LogResponse.model_validate(log_dict)

@router.get("/user/{id}", response_model=List[LogResponse], status_code=status.HTTP_200_OK)
async def get_all_logs_by_user_id(
    id: int,
    question_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    log_service: LogService = Depends(get_log_service)
) -> List[LogResponse]:
    """Retrieve all logs by user"""
    logs_list_dict = await log_service.get_logs_by_user_id(id=id, question_id=question_id, skip=skip, limit=limit)
    if logs_list_dict == None:
        raise HTTPException(status_code=400, detail="No logs found for user")
    return [LogResponse.model_validate(log_dict) for log_dict in logs_list_dict]

