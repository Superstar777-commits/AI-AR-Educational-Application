"""
    Quiz router Pydantic schema
"""

from pydantic import BaseModel
from typing import Optional

class QuizBase(BaseModel):
    title: str
    duration: int

# No added parameters as the base has all of them therefore just pass
class QuizCreate(QuizBase):
    pass

class QuizUpdate(QuizBase):
    pass

# Schema for quiz response
class QuizResponse(QuizBase):
    id: int

    # pydantic config to allow ORM mode
    # allows PyDantic to read attributes directly from SQLAlchemy Core Row objects (or ORM instances)
    class Config:
        from_attributes = True