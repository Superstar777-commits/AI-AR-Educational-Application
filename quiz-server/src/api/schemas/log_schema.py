from pydantic import BaseModel
from datetime import datetime

class LogBase(BaseModel):
    action: str
    time: datetime
    user_id: int
    question_id: int

class LogCreate(LogBase):
    action: str
    time: datetime
    user_id: int
    question_id: int

class LogResponse(LogBase):
    id: int

    class Config:
        from_attributes = True