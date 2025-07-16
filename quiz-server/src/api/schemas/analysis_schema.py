from pydantic import BaseModel

class AnalysisBase(BaseModel):
    user_id: int
    question_id: int
    analysis: str

class AnalysisCreate(AnalysisBase):
    user_id: int
    question_id: int
    analysis: str

class AnalysisResponse(AnalysisBase):
    id: int

    class Config:
        from_attributes = True