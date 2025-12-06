from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_spotify_configured(self) -> bool:
        return bool(self.SPOTIFY_CLIENT_ID and self.SPOTIFY_CLIENT_SECRET)

settings = Settings()
