from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table, TIMESTAMP
from ..core.database import metadata
import enum

class Actions(enum.Enum):
    pause = 1
    resume = 2
    started = 3
    completed = 4

logs_table = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("action", Enum(Actions), nullable=False),
    Column("time", TIMESTAMP, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("question_id", Integer, ForeignKey("Question.id"), nullable=False)
)