from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = "sk-your-key-here"
    cors_origins: list[str] = ["http://localhost:3000", "https://your-frontend.vercel.app"]
    environment: str = "development"
    docs_dir: str = "docs"


settings = Settings()
