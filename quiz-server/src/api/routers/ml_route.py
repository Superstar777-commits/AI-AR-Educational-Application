"""
    File handles all the routes that will access all the ML model's functions, e.g. classification, trend analysis
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from pandas import DataFrame

from src.services.ml_service import MLService
from src.api.schemas.ml_schema import MLResponse
from src.api.dependencies.common import get_ml_service

router = APIRouter(prefix="/ml", tags=["ML"])

@router.get("/df/{id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_df(
    id: int,
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    ml_service: MLService = Depends(get_ml_service)
) -> List[Dict[str, Any]]:
    """
        Create and return a DataFrame, using the quiz id (id) and a user id as a filter
    """
    dfs = await ml_service.analyse(id=id)
    if dfs == None:
        raise HTTPException(status_code=500, detail="Something went wrong")
    print(dfs)
    return dfs