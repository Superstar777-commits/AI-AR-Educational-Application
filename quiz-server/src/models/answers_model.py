from sqlalchemy import Column, Integer, String, Table, ForeignKey
from ..core.database import metadata

answers_table = Table(
    "answers",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("question_id", Integer, ForeignKey("Question.id"), nullable=False),
    Column("answer", String, nullable=True),
    Column("marksAchieved", Integer, nullable=True)
)