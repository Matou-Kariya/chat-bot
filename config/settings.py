from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.redmi"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_DATABASE: str

    # LLM
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = ""
    DEEPSEEK_MODEL: str = ""
    DASHSCOPE_API_KEY: str = ""
    QWEN_BASE_URL: str = ""
    QWEN_CHAT_MODEL: str = ""
    QWEN_IMAGE_MODEL: str = ""
    QWEN_ASR_MODEL: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
