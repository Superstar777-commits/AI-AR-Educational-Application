"""
    Answer router Pydantic schema
"""

from pydantic import BaseModel
from typing import Optional

# Base schema
class AnswerBase(BaseModel):
    question_id: int
    user_id: int
    quiz_id: int
    answer: str


class AnswerCreate(AnswerBase):
    question_id: int
    user_id: int
    quiz_id: int
    answer: str

class AnswerUpdate(AnswerBase):
    id: int
    marksAchieved: int

class AnswerResponse(AnswerBase):
    id: int
    marks: Optional[int] = None
    marksAchieved: Optional[int] = None
    question: Optional[str] = None
    correctAnswer: Optional[str] = None

    class Config:
        from_attributes = True