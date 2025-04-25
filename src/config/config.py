from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Config(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()