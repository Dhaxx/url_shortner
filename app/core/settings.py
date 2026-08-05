from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "URL Shortener"
    debug: bool = False

    # DB Application
    db_host: str = "localhost"
    db_user: str = "sysdba"
    db_password: str = "masterkey"
    db_name: str = "/data/app.db"
    sgbd_driver: str = "sqlite"

    # Security
    secret_key: str = ""
    jwt_secret_key: str = "super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480

    # Redis 
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    short_url_ttl_seconds: int = 3600

    @property
    def db_url(self) -> str:
        if self.sgbd_driver == "sqlite":
            return f"sqlite:///{self.db_name}"
        else:
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def time_now(self) -> datetime:
        return (
            datetime.now(ZoneInfo("UTC"))
            .astimezone(ZoneInfo("America/Sao_Paulo"))
            .replace(tzinfo=None)
        )

    @property
    def time_now_prop(self) -> datetime:
        return self.time_now()

    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings()