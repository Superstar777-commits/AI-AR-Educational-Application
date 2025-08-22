"""
    Question router Pydantic schema
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import time

class QuestionBase(BaseModel):
    question: str
    marks: int
    level: str
    correctAnswer: str
    quiz_id: int
    type: str

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    question: str
    marks: int
    correctAnswer: str

class QuestionResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True

