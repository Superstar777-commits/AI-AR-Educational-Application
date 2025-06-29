from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema for common user attributes
class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str

# schema for creating a new user (input model for POST reqeuests)
# omits id as the db generates one
# Schema for creating a new user (requires password)
class UserCreate(UserBase):
    password: str

# Schema for updating an existing user
class UserUpdate(UserBase):
    password: Optional[str] = None

# schema for user response
# includes auto-generated ID
class UserResponse(UserBase):
    id: int

    # pydantic config to allow ORM mode
    # allows PyDantic to read attributes directly from SQLAlchemy Core Row objects (or ORM instances)
    class Config:
        from_attributes = True