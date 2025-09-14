"""
    File handles all the routes for the User table
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional

# Import Pydantic schemas for request and response data
from src.api.schemas.user_schema import UserCreate, UserResponse, UserUpdate
# Import the UserService, which contains the business logic
from src.services.user_service import UserService
# Import the dependency to inject the UserService
from src.api.dependencies.common import get_user_service
from src.api.dependencies.auth import verify_firebase_token, validate_current_user
from src.api.schemas.auth_schema import FirebaseUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Create a new user.
    Expects UserCreate schema  as input.
    Returns UserResponse schema on success, or 400 if user already exists.
    """
    user_dict = await user_service.create_user(user_data)
    print(f"User dict: {user_dict}")
    if user_dict == None:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    return UserResponse.model_validate(user_dict) # Convert dict from service to Pydantic model

@router.get("/all", response_model=List[UserResponse])
async def get_all_users_route(
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[Dict[str, Any]] = Depends(validate_current_user),
    user_service: UserService = Depends(get_user_service)
) -> List[UserResponse]:
    """
    Retrieve a list of all users with pagination.
    """
    if not current_user or current_user['type'].value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    users_list_dict = await user_service.get_all_users(skip=skip, limit=limit)
    print(f"Users list dict: {users_list_dict}")
    # Convert each user dictionary in the list to a UserResponse Pydantic model
    return [UserResponse.model_validate(user_dict) for user_dict in users_list_dict]

@router.get("/user/email", response_model=UserResponse)
async def get_user_by_email_route(
    firebase_user: FirebaseUser = Depends(verify_firebase_token),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Retrieve a user by their ID.
    Returns UserResponse schema on success, or 404 if not found.
    """
    if not firebase_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    print(firebase_user)
    user_dict = await user_service.get_user_by_email(firebase_user.email)
    if not user_dict:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse.model_validate(user_dict) # Convert dict from service to Pydantic model

@router.get("/{id}", response_model=UserResponse)
async def get_user_route(
    id: int,
    firebase_user: Optional[Dict[str, Any]] = Depends(verify_firebase_token),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Retrieve a user by their ID.
    Returns UserResponse schema on success, or 404 if not found.
    """
    if not firebase_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    user_dict = await user_service.get_user_by_id(id)
    if not user_dict:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse.model_validate(user_dict) # Convert dict from service to Pydantic model

@router.put("/{id}", response_model=UserResponse)
async def update_user_route(
    id: int,
    user_data: UserUpdate,
    current_user: Optional[Dict[str, Any]] = Depends(validate_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Update an existing user by their ID.
    Expects UserUpdate schema as input.
    Returns updated UserResponse schema on success, or 404 if not found.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    updated_user_dict = await user_service.update_user(id, user_data)
    if not updated_user_dict:
        raise HTTPException(status_code=404, detail="User not found or nothing to update.")
    return UserResponse.model_validate(updated_user_dict)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(
    id: int,
    current_user: Optional[Dict[str, Any]] = Depends(validate_current_user),
    user_service: UserService = Depends(get_user_service)
) -> None:
    """
    Delete a user by their ID.
    Returns 204 No Content on successful deletion, or 404 if not found.
    """
    if not current_user or current_user['type'].value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    deleted = await user_service.delete_user(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found.")
