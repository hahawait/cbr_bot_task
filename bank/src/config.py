from dataclasses import dataclass
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class RedisConfig(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class BankConfig(BaseConfig):
    URL: str
    EXCHANGE_RATES_ENDPOINT: str


@dataclass
class Config:
    bank_config: BankConfig
    redis_config: RedisConfig


@lru_cache
def get_config():
    return Config(
        bank_config=BankConfig(),
        redis_config=RedisConfig()
    )
