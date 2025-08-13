"""
    Model for qoptions table
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from ..core.database import metadata

qoptions_table = Table(
    "qoptions",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("option", String, nullable=False),
    Column("question_id", Integer, ForeignKey("questions.id"), nullable=False)
)