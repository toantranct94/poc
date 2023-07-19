import json
from typing import Any

import redis

from app.core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    db=settings.redis_db
)


class CacheService():

    @staticmethod
    def get(key: str) -> Any:
        value = redis_client.get(key)
        if value:
            return value.decode()
        return None

    @staticmethod
    def insert(key: str, value: Any) -> None:
        redis_client.set(key, CacheService.__standalize(value))

    @staticmethod
    def __standalize(value: Any) -> str:
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value)
        else:
            return value
