from pydantic import BaseModel, Field
from typing import Optional

class FirebaseUser(BaseModel):
    """
    Represents an authenticated user from Firebase
    """
    uid: str = Field(..., description="The unique user ID from Firebase.")
    email: str = Field(..., description="THe user's email address.")