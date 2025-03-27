from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings(EnvBaseSettings):
    BOT_TOKEN: str


class PostgresSettings(EnvBaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DB,
        )


class RedisSettings(EnvBaseSettings):
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: str

    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            username=self.REDIS_USER,
            password=self.REDIS_PASSWORD,
            path=self.REDIS_DB,
        )


class Settings(BotSettings, PostgresSettings, RedisSettings):
    DEBUG: bool


settings = Settings()
