"""
    Log router Pydantic schema
"""

from pydantic import BaseModel
from datetime import datetime
from src.models.logs_model import Actions

class LogBase(BaseModel):
    action: Actions
    time: datetime
    user_id: int
    question_id: int

class LogCreate(LogBase):
    pass

class LogUpdate(LogBase):
    pass

class LogResponse(LogBase):
    id: int

    class Config:
        from_attributes = True