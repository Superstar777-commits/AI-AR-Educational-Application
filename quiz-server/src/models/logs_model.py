"""
    Model for Logs table
"""

from sqlalchemy import Column, Integer, Enum, ForeignKey, Table, TIMESTAMP
from ..core.database import metadata
import enum

# Enum for log action
class Actions(enum.Enum):
    pause = "pause"
    resume = "resume"
    started = "started"
    completed = "completed"

logs_table = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("action", Enum(Actions), nullable=False),
    Column("time", TIMESTAMP, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("question_id", Integer, ForeignKey("Question.id"), nullable=False)
)