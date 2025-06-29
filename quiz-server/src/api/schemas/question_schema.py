from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import time

class QuestionBase(BaseModel):
    id: int
    question: str
    marks: int
    level: str
    correctAnswer: str
    done: bool
    startTime: Optional[datetime]
    endTime: Optional[datetime]
    quiz_id: int

class QuestionCreate(QuestionBase):
    question: str
    marks: int
    level: str
    correctAnswer: str
    quiz_id: int

class QuestionUpdate(QuestionBase):
    question: str
    marks: int
    done: bool
    correctAnswer: str

class MarkAsDone(QuestionBase):
    done: bool

class QuestionResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True

