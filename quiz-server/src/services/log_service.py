"""
    Service for Logs
    Contains all the logic for the log_router
"""

from typing import Optional, List, Dict, Any
from src.api.schemas.log_schema import LogCreate, LogResponse
from src.repositories.log_repository import LogRepository

class LogService:
    def __init__(self, log_repo: LogRepository) -> None:
        self.log_repo = log_repo

    async def create_log(self, log_data: LogCreate) -> Optional[Dict[str, Any]]:
        """Creates a new log"""
        log_dict = await self.log_repo.create_log(log_data=log_data)
        return log_dict

    async def get_log_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        question_dict = await self.log_repo.get_log_by_id(id)
        return question_dict

    async def get_logs_by_user_id(self, id: int, skip: int=0, limit: int=10):
        """Retrieves logs by user id"""
        log_list_dict = await self.log_repo.get_logs_by_user_id(id, skip, limit)
        return log_list_dict

    async def get_logs(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        """Retrieves all logs"""
        log_list_dict = await self.log_repo.get_logs(skip, limit)
        return log_list_dict