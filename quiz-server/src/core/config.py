"""
    Handles all the settings and connection string
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# use find_dotenv() to locate .env file by searching upwards from the current directory
# this ensures it works no matter where the script is being run from
load_dotenv(find_dotenv())

class Settings(BaseSettings):
    """
    Project settings loading from env variables
    """
    # DATABASE_URL should use 'mysql+pymysql' dialect for synchronous connection
    DATABASE_URL: str
    FIREBASE_SERVICE_ACCOUNT: str

    # this setting helps pydantic_settings find the variables
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings() # type: ignore