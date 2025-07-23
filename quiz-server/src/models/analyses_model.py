"""
    Model for Analyses table
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from ..core.database import metadata

analyses_table = Table(
    "analyses",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("question_id", Integer, ForeignKey("Question.id"), nullable=False),
    Column("analysis", String, nullable=False)
)