"""
    Repository for Users
    Contains all the concrete implementations for users_service functions
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from starlette.concurrency import run_in_threadpool # essential for sync calls

from ..models.user_model import users_table
from ..api.schemas.user_schema import UserCreate, UserResponse, UserUpdate  # Pydantic schemas for input

class UserRepository:
    def __init__(self, db: Session): # expect a synchronous session
        self.db = db

    async def create_user(self, user_data: UserCreate) -> Dict[str, Any] | None:
        """Creates a new user record  using SQLAlchemy Core"""
        def _create_user_sync():
            # in real app hash password in service layer before passing to repo
            stmt = insert(users_table).values(
                email = user_data.email,
                password = user_data.password,
                name = user_data.name,
                surname = user_data.surname
            )

            result = self.db.execute(stmt)
            self.db.commit() # commit transaction

            # For SQLAlchemy Core, getting the inserted ID often requires fetching it
            # if not directly returned by dialect.  More robust way is to use RETURNING (if supported by dialect) or a separate select

            # fetch the created user to return its full data including generated ID
            created_user_row = self.db.execute(
                select(users_table).where(users_table.c.id == result.lastrowid)
            ).first()

            return created_user_row._asdict() if created_user_row else None # convert row to dict

        return await run_in_threadpool(_create_user_sync)

    async def get_user_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a user by ID using SQLAlchemy Core"""
        def _get_user_by_id_sync():
            stmt = select(users_table).where(users_table.c.id == id)
            user_row = self.db.execute(stmt).first()
            return user_row._asdict() if user_row else None

        return await run_in_threadpool(_get_user_by_id_sync)

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieves a user by email using SQLAlchemy Core"""
        def _get_user_by_email_sync():
            stmt = select(users_table).where(users_table.c.email == email)
            user_row = self.db.execute(stmt).first()
            print(f"User Row: {user_row}")
            return user_row._asdict() if user_row else None

        return await run_in_threadpool(_get_user_by_email_sync)

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves a list of users using SQLAlchemy Core"""
        def _get_users_sync():
            stmt = select(users_table).offset(skip).limit(limit)
            results = self.db.execute(stmt).fetchall()
            return [row._asdict() for row in results]

        return await run_in_threadpool(_get_users_sync)

    async def update_user(self, id: int, user_data: UserUpdate) -> Optional[Dict[str, Any]]:
        """Updates a user record using SQLAlchemy Core."""
        def _update_user_sync():
            # Create a dictionary of non-None values from user_data
            update_values = {k: v for k, v in user_data.model_dump(exclude_unset=True).items() if v is not None}

            if not update_values: # No data to update
                user_row = self.db.execute(select(users_table).where(users_table.c.id == id)).first()
                return user_row._asdict() if user_row else None


            stmt = update(users_table).where(users_table.c.id == id).values(**update_values)
            self.db.execute(stmt)
            self.db.commit()

            # Fetch the updated user to return its current data
            updated_user_row = self.db.execute(
                select(users_table).where(users_table.c.id == id)
            ).first()
            return updated_user_row._asdict() if updated_user_row else None

        return await run_in_threadpool(_update_user_sync)

    async def delete_user(self, id: int) -> bool:
        """Deletes a user record using SQLAlchemy Core."""
        def _delete_user_sync():
            stmt = delete(users_table).where(users_table.c.id == id)
            result = self.db.execute(stmt)
            self.db.commit()
            return result.rowcount > 0 # Return True if a row was deleted

        return await run_in_threadpool(_delete_user_sync)