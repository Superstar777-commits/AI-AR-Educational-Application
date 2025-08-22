"""
    Service for Users
    Contains all the logic for the user_router
"""

from typing import Optional, List, Dict, Any
# remember to get hashing lib

# import pydantic schemas for input/output
from src.api.schemas.user_schema import UserUpdate, UserCreate, UserResponse

# import UserRepository for data access
from src.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate) -> Optional[Dict[str, Any]]:
        """
            Creates a new user, handles business logic like checking for exisiting email.
            hashes the password before sending to repository
        """

        # business logic: check if user with this email already exists
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        print(f"Existing user: {existing_user}")
        if existing_user:
            return None # indicate conflict, router will handle http 400
        # in a real app, hash the password here

        # call the repo to create the user
        # the repo now returns a dict (or None)
        user_dict = await self.user_repo.create_user(user_data)
        return user_dict

    async def get_user_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a user by  ID
        returns a dict representation of the user or None if not found
        """
        user_dict = await self.user_repo.get_user_by_id(id)
        return user_dict

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a user by email
        returns a dict representation of the user or None if not found
        """
        user_dict = await self.user_repo.get_user_by_email(email)
        return user_dict

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieves all users with pagination
        Returns a list of user dictionaries
        """
        users_list_dict = await self.user_repo.get_users(skip=skip, limit=limit)
        print(f"Users list: {users_list_dict}")
        return users_list_dict

    async def update_user(self, id: int, user_data: UserUpdate) -> Optional[Dict[str, Any]]:
        """
        Updates an existing user.
        Handles partial updates and passes to the repo
        """
        updated_user_dict = await self.user_repo.update_user(id, user_data)
        return updated_user_dict

    async def delete_user(self, id: int) -> bool:
        """
        Deletes a user by ID.
        Returns True on successful deletion, False otherwise
        """
        deleted = await self.user_repo.delete_user(id)
        return deleted