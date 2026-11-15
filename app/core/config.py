from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
<<<<<<< HEAD
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    DB_URL: str
    DB_SECRET_KEY: str
    KAFKA_BOOTSTRAP_SERVERS: str
    ECHO: bool


=======
    db_url: str
    db_secret_key: str
    kafka_bootstrap_servers: str
    echo: bool
    model_config = SettingsConfigDict(env_file=".env")
>>>>>>> dev

settings = Settings()