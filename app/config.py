"""
Application configuration
"""

from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings

    These are the defaults values that the application will use if the environment variables are not set.
    """

    # Default Database connection string
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ecommerce_db"

    # Default Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Default CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Default Application settings
    DEBUG: bool = False
    PROJECT_NAME: str = "FastAPI E-commerce"

    model_config = ConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
