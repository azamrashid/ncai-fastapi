from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL_NEON: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY_LENGTH: int = 32

    class Config:
        env_file = ".env"

settings = Settings()