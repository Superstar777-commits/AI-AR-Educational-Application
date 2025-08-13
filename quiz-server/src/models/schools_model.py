"""
    Model for schools table
"""

from sqlalchemy import Column, Integer, String, Enum, Table
from ..core.database import metadata
import enum

class Area(enum.Enum):
    urban = 'urban'
    rural = 'rural'
    township = 'township'
    suburban = 'suburban'

class Type(enum.Enum):
    public = 'public'
    private = 'private'

schools_table = Table(
    "schools",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, nullable=False),
    Column("province", String, nullable=False),
    Column("area", Enum(Area), nullable=False),
    Column("type", Enum(Type), nullable=False)
)