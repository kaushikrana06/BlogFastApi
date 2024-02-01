from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    database_url: str = "mongodb://localhost:27017"

    # Security
    secret_key: str = "a_very_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Add other settings as needed
    # ...

    class Config:
        # This option allows loading the environment variables
        # from a .env file, if available.
        env_file = ".env"

settings = Settings()
