"""
    Model for Users table
"""

from sqlalchemy import Column, Integer, String, Table, Enum, ForeignKey
from ..core.database import metadata # import Base from db setup
import enum

class Type(enum.Enum):
    student = 'student'
    teacher = 'teacher'
    admin = 'admin'

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("email", String(100), unique=True, nullable=False),
    Column("password", String(100), nullable=False),
    Column("name", String(100), nullable=False),
    Column("surname", String(100), nullable=False),
    Column("school_id", Integer, ForeignKey("schools.id"), nullable=True),
    Column("type", Enum(Type), nullable=False),
    Column("grade", Integer, nullable=True)
)