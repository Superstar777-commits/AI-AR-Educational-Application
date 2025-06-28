from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP, ForeignKey, Table
from ..core.database import metadata # import Base from db setup

quizzes_table = Table(
    "quizzes",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("title", String, nullable=False),
    Column("duration", Integer, nullable=False)
)