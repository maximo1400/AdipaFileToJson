from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

FALLBACK_GEMINI_MODEL = "gemini-3.5-flash-lite"


class Settings(BaseSettings):
    app_name: str = "Adipa File To Questionnaire JSON"
    version: str = "0.1.0"
    debug: bool = False

    # LLM Settings
    gemini_api_key: str = ""
    gemini_model: str | None = None
    fallback_model: str = FALLBACK_GEMINI_MODEL

    @property
    def effective_model(self) -> str:
        """Returns gemini_model from environment, or falls back to fallback_model if null or empty."""
        if self.gemini_model and self.gemini_model.strip():
            return self.gemini_model.strip()
        return self.fallback_model

    # Upload restrictions
    max_file_size_mb: int = 15
    allowed_extensions: list[str] = [".pdf", ".docx", ".xlsx"]

    # CORS
    allowed_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
