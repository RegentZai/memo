"""配置文件"""

from pydantic_settings import BaseSettings
from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    # Database
    SQLALCHEMY_DATABASE_URL: str
    # LogName
    ACCESS_LOG: str
    ERROR_LOG: str

    class Config:
        env_file = ".env"
        extra = "ignore"

class CORSConfig(BaseSettings):
    ALLOWED_ORIGINS: list = []
    ALLOWED_METHODS: list
    ALLOWED_HEADERS: list
    ALLOWED_CREDENTIALS: bool

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
corsConfig = CORSConfig()
limiter = Limiter(key_func=get_remote_address)
