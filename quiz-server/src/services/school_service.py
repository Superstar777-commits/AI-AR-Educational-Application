from typing import Optional, List, Dict, Any

from src.api.schemas.schools_schema import SchoolCreate, SchoolUpdate

from src.repositories.schools_repository import SchoolRepository

class SchoolService:
    def __init__(self, school_repo: SchoolRepository) -> None:
        self.school_repo = school_repo

    async def create_school(self, school_data: SchoolCreate) -> Optional[Dict[str, Any]]:
        school_dict = await self.school_repo.create_school(school_data)

        return school_dict

    async def get_school(self, id: int) -> Optional[Dict[str, Any]]:
        school_dict = await self.school_repo.get_school_by_id(id)
        return school_dict

    async def get_schools(self, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        schools = await self.school_repo.get_schools(skip, limit)
        return schools

    async def update_school(self, id: int, school_data: SchoolUpdate) -> Optional[Dict[str, Any]]:
        school_dict = await self.school_repo.update_school(id, school_data)
        return school_dict

