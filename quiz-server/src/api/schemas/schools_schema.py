"""
    School router Pydantic schema
"""

from pydantic import BaseModel

class SchoolBase(BaseModel):
    name: str
    province: str
    area: str
    type: str

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(SchoolBase):
    pass

class SchoolResponse(SchoolBase):
    id: int

    class Config:
        from_attributes = True