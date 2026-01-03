from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DISCOGS_CONSUMER_KEY: str = ""
    DISCOGS_CONSUMER_SECRET: str = ""
    GEMINI_API_KEY: str = "" # Optional: If empty, curation is skipped
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500"] # Default dev origins

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_discogs_configured(self) -> bool:
        return bool(self.DISCOGS_CONSUMER_KEY and self.DISCOGS_CONSUMER_SECRET)

settings = Settings()
