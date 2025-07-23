"""
    Model for Analyses table
"""

from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..core.database import metadata # import Base from db setup
import enum

# Enum for question levels
class Levels(enum.Enum):
    low = 1
    medium = 2
    high = 3

questions_table = Table(
    "questions",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("quiz_id", Integer, ForeignKey("Quiz.id"), nullable=False),
    Column("question", String, nullable=False),
    Column("marks", Integer, nullable=False),
    Column("level", Enum(Levels), nullable=False, default=Levels.low),
    Column("correctAnswer", String, nullable=False)
)