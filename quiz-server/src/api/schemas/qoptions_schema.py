"""
    QOptions router Pydantic schema
"""

from pydantic import BaseModel

class QOPtionsBase(BaseModel):
    option: str
    question_id: int

class QOptionsCreate(QOPtionsBase):
    pass

class QOptionsUpdate(QOPtionsBase):
    pass

class QOptionsResponse(QOPtionsBase):
    id: int

    class Config:
        from_attributes = True