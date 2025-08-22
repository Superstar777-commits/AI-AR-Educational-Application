"""
    Handles all the settings and connection string
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Determine the project root for .env file location
    # Assumes .env is in the mono-repo root (parent of 'quiz-server')
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / '.env',
        env_file_encoding='utf-8'
    )

    # DATABASE_URL should use 'mysql+pymysql' dialect for synchronous connection
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/neurostemdb"

settings = Settings()