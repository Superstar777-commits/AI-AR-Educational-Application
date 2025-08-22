from typing import Optional, List, Dict, Any

from src.api.schemas.qoptions_schema import QOptionsCreate, QOptionsUpdate
from src.repositories.qoptions_repository import QOptionsRepository

class QOPtionService:
    def __init__(self, qopt_repo: QOptionsRepository) -> None:
        self.qopt_repo = qopt_repo

    async def create_qopt(self, qopt_data: QOptionsCreate) -> Optional[Dict[str, Any]]:
        qopt_dict = await self.qopt_repo.create_qoption(qopt_data=qopt_data)
        return qopt_dict

    async def get_qopt(self, id: int) -> Optional[Dict[str, Any]]:
        qopt_dict = await self.qopt_repo.get_qoption_by_id(id)
        return qopt_dict

    async def get_qopts_by_question(self, q_id: int, skip: int=0, limit: int=10) -> List[Dict[str, Any]]:
        qopts = await self.qopt_repo.get_qoptions_by_question(q_id, skip, limit)
        return qopts

    async def update_qopt(self, id: int, qopt_data: QOptionsUpdate):
        qopt_dict = await self.qopt_repo.update_qopt(id, qopt_data)
        return qopt_dict
