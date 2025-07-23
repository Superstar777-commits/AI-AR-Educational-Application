"""
    Model for Users table
"""

from sqlalchemy import Column, Integer, String, Table
from ..core.database import metadata # import Base from db setup

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("email", String(45), unique=True, nullable=False),
    Column("password", String(45), nullable=False),
    Column("name", String(45), nullable=False),
    Column("surname", String(45), nullable=False),
)