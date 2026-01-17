"""Application config"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration."""
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )


config = Config()  # type: ignore
