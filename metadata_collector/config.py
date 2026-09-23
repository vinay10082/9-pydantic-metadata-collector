from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    strict_validation_mode: bool = True
    metadata_ingestion_port: int = 8000


settings = Settings()
