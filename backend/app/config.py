from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./book.db"
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()