"""
    Analysis router Pydantic schema
"""

from pydantic import BaseModel

class AnalysisBase(BaseModel):
    user_id: int
    question_id: int
    analysis: str

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisUpdate(AnalysisBase):
    pass

class AnalysisResponse(AnalysisBase):
    id: int

    class Config:
        from_attributes = True