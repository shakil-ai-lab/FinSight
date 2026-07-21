from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # Application Settings
    # ==========================================================
    APP_NAME: str = "FinSight"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # ==========================================================
    # AI Model Configuration
    # ==========================================================
    MODEL_PROVIDER: str = "gemini"
    MODEL_NAME: str = "gemini-2.5-flash"

    # ==========================================================
    # API Keys
    # ==========================================================
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    HUGGINGFACE_API_KEY: str | None = None

    # ==========================================================
    # Vector Database
    # ==========================================================
    CHROMA_DB_PATH: str = "./data/chroma"

    # ==========================================================
    # SQLite Database
    # ==========================================================
    DATABASE_URL: str = "sqlite:///./data/finsight.db"

    # ==========================================================
    # SEC Configuration
    # ==========================================================
    SEC_USER_AGENT: str = "FinSight/1.0 sanjaralap@gmail.com"
    SEC_TIMEOUT: int = 30


settings = Settings()