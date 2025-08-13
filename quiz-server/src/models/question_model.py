"""
    Model for Analyses table
"""

from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..core.database import metadata # import Base from db setup
import enum

# Enum for question levels
class Levels(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class Type(enum.Enum):
    text = 'text'
    mc = 'mc'
    tf = 'tf'

questions_table = Table(
    "questions",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("quiz_id", Integer, ForeignKey("Quiz.id"), nullable=False),
    Column("question", String, nullable=False),
    Column("marks", Integer, nullable=False),
    Column("level", Enum(Levels), nullable=False, default=Levels.low),
    Column("correctAnswer", String, nullable=False),
    Column("type", Enum(Type), nullable=False, default=Type.text)
)