# Loads environment variables into Python settings object.
# Centralized config management.

from pydantic_settings import BaseSettings
from pydantic_settings import (
    SettingsConfigDict
)

class Settings(BaseSettings):

    DATABASE_URL: str

    REDIS_URL: str

    MAX_PAYMENT_RETRIES: int = 3        #Defines maximum retry attempts

    PAYMENT_RETRY_DELAY: int = 10       # Defines delay before retry

    JWT_SECRET_KEY: str

    JWT_ALGORITHM: str
    
    JWT_EXPIRATION_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
