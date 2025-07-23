"""
    Service for Analyses
    Contains all the logic for the analysis_router
"""

from typing import Optional, List, Dict, Any
from src.api.schemas.analysis_schema import AnalysisCreate
from src.repositories.analysis_repository import AnalysisRepository

class AnalysisService:
    def __init__(self, analysis_repo: AnalysisRepository) -> None:
        self.analysis_repo = analysis_repo

    async def create_analysis(self, analysis_data: AnalysisCreate) -> Optional[Dict[str, Any]]:
        """Creates a new analysis"""
        analysis_dict = await self.analysis_repo.create_analysis(analysis_data=analysis_data)
        return analysis_dict

    async def get_analysis_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """"Retrieves an analysis by ID"""
        analysis_dict = await self.analysis_repo.get_analysis_by_id(id)
        return analysis_dict

    async def get_analyses_by_user_id(self, id: int, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        analysis_list_dict = await self.analysis_repo.get_analyses_by_user_id(id=id, skip=skip, limit=limit)
        return analysis_list_dict