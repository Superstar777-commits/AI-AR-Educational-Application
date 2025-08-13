"""
    Model for topics table
"""

from sqlalchemy import Column, Integer, String, Table
from ..core.database import metadata

topics_table = Table(
    "topics",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, nullable=False),
    Column("details", String, nullable=False)
)