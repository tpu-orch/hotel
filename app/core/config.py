from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    db_url: str
    db_secret_key: str
    kafka_bootstrap_servers: str
    echo: bool
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()