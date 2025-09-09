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
    marks: int
    marksAchieved: int
    question: str
    correctAnswer: str
    type: str

    class Config:
        from_attributes = True