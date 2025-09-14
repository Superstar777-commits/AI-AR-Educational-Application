"""
    Repository for Users
    Contains all the concrete implementations for users_service functions
"""

from typing import Optional, List, Dict, Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import Row

from src.models.user_model import users_table
from src.api.schemas.user_schema import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: AsyncSession):
        """
        Initializes the repository with an asynchronous database session.
        """
        self.db = db
        print(f"User repository initialized with session: {self.db}")

    async def create_user(self, user_data: UserCreate) -> Dict[str, Any] | None:
        """
        Asynchronously creates a new user record using SQLAlchemy Core.
        """
        try:
            stmt = insert(users_table).values(
                email=user_data.email,
                password=user_data.password,
                name=user_data.name,
                surname=user_data.surname,
                grade=user_data.grade,
                type=user_data.type,
                school_id=user_data.school_id
            )

            # Execute the insert statement and await the result
            result = await self.db.execute(stmt)
            await self.db.commit()

            # Get the ID of the newly created row
            new_user_id = result.lastrowid

            # Fetch and return the newly created user
            return await self.get_user_by_id(new_user_id)
        except Exception as e:
            await self.db.rollback()
            print(f"Error creating user: {e}")
            return None

    async def get_user_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Asynchronously retrieves a user by ID.
        """
        try:
            stmt = select(users_table).where(users_table.c.id == id)
            # Await the execution and then fetch the first result
            result = await self.db.execute(stmt)
            user_row: Optional[Row] = result.first()
            return user_row._asdict() if user_row else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Asynchronously retrieves a user by email.
        """
        try:
            stmt = select(users_table).where(users_table.c.email == email)
            # Await the execution and then fetch the first result
            result = await self.db.execute(stmt)
            user_row: Optional[Row] = result.first()
            print(f"User Row: {user_row}")
            return user_row._asdict() if user_row else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Asynchronously retrieves a list of users.
        """
        try:
            stmt = select(users_table).offset(skip).limit(limit)
            # Await the execution and then fetch all results
            result = await self.db.execute(stmt)
            users: Sequence[Row] = result.fetchall()
            print(f"Results: {users}")
            return [row._asdict() for row in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    async def update_user(self, id: int, user_data: UserUpdate) -> Optional[Dict[str, Any]]:
        """
        Asynchronously updates a user record.
        """
        try:
            update_values = user_data.model_dump(exclude_unset=True)
            if not update_values:
                return await self.get_user_by_id(id)

            stmt = update(users_table).where(users_table.c.id == id).values(**update_values)

            # Await the execution of the update statement
            await self.db.execute(stmt)
            await self.db.commit()

            # Fetch and return the updated user
            return await self.get_user_by_id(id)
        except Exception as e:
            await self.db.rollback()
            print(f"Error updating user: {e}")
            return None

    async def delete_user(self, id: int) -> bool:
        """
        Asynchronously deletes a user record.
        """
        try:
            stmt = delete(users_table).where(users_table.c.id == id)
            # Await the execution of the delete statement
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            await self.db.rollback()
            print(f"Error deleting user: {e}")
            return False
