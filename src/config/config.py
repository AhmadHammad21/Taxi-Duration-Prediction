from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal
from pydantic import Field


class Config(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None

    APP_ENV: Literal["dev", "qa", "uat", "prod"] = Field(default="dev")
    
    # Environment-specific MLflow settings
    MLFLOW_TRACKING_URI_LAMBDA: str = "file:///tmp/mlflow"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
