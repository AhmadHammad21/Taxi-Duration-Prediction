from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal
from pydantic import Field

class Config(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None

    APP_ENV: Literal["dev", "qa", "uat", "prod"] = Field(default="dev")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()