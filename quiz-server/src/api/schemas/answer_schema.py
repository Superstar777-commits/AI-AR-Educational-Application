"""
    Answer router Pydantic schema
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema
class AnswerBase(BaseModel):
    question_id: int
    user_id: int
    quiz_id: int
    answer: str
    marksAchieved: Optional[int] = None
    question: Optional[str] = None

class AnswerCreate(AnswerBase):
    question_id: int
    user_id: int
    quiz_id: int
    answer: str

class AnswerUpdate(AnswerBase):
    id: int
    marks: int

class AnswerResponse(AnswerBase):
    id: int

    class Config:
        from_attributes = True