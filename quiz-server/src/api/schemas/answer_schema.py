from pydantic import BaseModel
from typing import Optional

# Base schema
class AnswerBase(BaseModel):
    question_id: int
    user_id: int
    answer: str
    marksAchieved: Optional[int] = None

class AnswerCreate(AnswerBase):
    question_id: int
    user_id: int
    answer: str

class AnswerResponse(AnswerBase):
    id: int

    class Config:
        from_attributes = True