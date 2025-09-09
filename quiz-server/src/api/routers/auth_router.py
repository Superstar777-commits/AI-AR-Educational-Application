from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

#from src.api.schemas.auth_schema import AuthRequest, AuthResponse
from src.services.user_service import UserService

from src.api.dependencies.common import get_user_service
from src.api.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
