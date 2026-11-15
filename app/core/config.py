from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    DB_URL: str
    DB_SECRET_KEY: str
    KAFKA_BOOTSTRAP_SERVERS: str
    ECHO: bool



settings = Settings()