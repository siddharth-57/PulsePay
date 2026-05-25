# Loads environment variables into Python settings object.
# Centralized config management.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    REDIS_URL: str

    MAX_PAYMENT_RETRIES: int = 3        #Defines maximum retry attempts

    PAYMENT_RETRY_DELAY: int = 10       # Defines delay before retry

    class Config:
        env_file = ".env"


settings = Settings()
