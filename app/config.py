from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str = "sqlite+aiosqlite:///./app.db"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()  # type: ignore[call-arg]