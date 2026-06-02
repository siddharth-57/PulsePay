# Loads environment variables into Python settings object.
# Centralized config management.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    REDIS_URL: str

    MAX_PAYMENT_RETRIES: int = 3        #Defines maximum retry attempts

    PAYMENT_RETRY_DELAY: int = 10       # Defines delay before retry

    JWT_SECRET_KEY: str = (
    "pulsepay-super-secret-key")

    JWT_ALGORITHM: str = "HS256"

    JWT_EXPIRATION_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
