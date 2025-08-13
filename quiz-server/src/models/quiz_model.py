"""
    Model for Quizzes table
"""

from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP, ForeignKey, Table
from ..core.database import metadata # import Base from db setup

quizzes_table = Table(
    "quizzes",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("duration", Integer, nullable=False),
    Column("grade", Integer, nullable=False),
    Column("school_id", Integer, ForeignKey("schools.id"), nullable=True),
    Column("topic_id", Integer, ForeignKey("topics.id"), nullable=False)
)