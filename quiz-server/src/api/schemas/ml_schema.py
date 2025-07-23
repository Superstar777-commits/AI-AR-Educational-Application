"""
    ML router Pydantic schema
"""

from pydantic import BaseModel
from typing import Optional, List
from pandas import DataFrame

class MLBase(BaseModel):
    user_id: Optional[int] = None
    input_data: str


class MLResponse(MLBase):
    user_id: Optional[int] = None
    input_data: str
    class Config:
        from_attributes = True