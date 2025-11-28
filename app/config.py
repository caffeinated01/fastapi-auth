from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")

    ALGORITHM: str
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: int

    CORS_ORIGINS: list[str]

    DATABASE_URL: str = f"sqlite:///{PROJECT_DIR}/database.db"


settings = Settings()  # type: ignore
