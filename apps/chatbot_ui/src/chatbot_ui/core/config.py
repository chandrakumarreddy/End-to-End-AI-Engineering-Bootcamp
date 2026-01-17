"""pydantic donfig"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration."""
    OPENAI_API_KEY: str
    BACKEND_API: str = 'http://api:8000'

    model_config = SettingsConfigDict(
        extra='ignore'
    )


config = Config()  # pyright: ignore
