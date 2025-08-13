"""
    Topic router Pydantic schema
"""

from pydantic import BaseModel

class TopicBase(BaseModel):
    name: str
    details: str

class TopicCreate(TopicBase):
    pass

class TopicUpdate(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: int

    class Config:
        from_attributes = True