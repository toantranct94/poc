import json
from typing import Any
import redis
import random

from cache.core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    db=settings.redis_db
)


class CacheService:
    @staticmethod
    def get(key: str) -> any:
        value = redis_client.get(key)

        if value is None:
            return value

        value_decoded = json.loads(value.decode('utf8'))
        return value_decoded

    @staticmethod
    def set(key: str, value: dict, ttl: int) -> None:
        value_str = CacheService.__standalize(value)
        if ttl == 0:
            # Add cache jitter to avoid cache avalanche
            jitter = random.randint(0, 60)
            ttl = settings.default_cache_ttl + jitter
        elif ttl == -1:
            redis_client.persist(key)
            return

        redis_client.setex(key, ttl, value_str)

    # @staticmethod
    # def insert(key: str, value: Any, ttl: int = None) -> None:
    #     value_str = CacheService.__standalize(value)
    #     if ttl is None:
    #         # Add cache jitter to avoid cache avalanche
    #         jitter = random.randint(0, 60)
    #         ttl = settings.default_cache_ttl + jitter
    #
    #     redis_client.setex(key, ttl, value_str)

    @staticmethod
    def delete(key: str) -> None:
        redis_client.delete(key)

    @staticmethod
    def exists(key: str) -> bool:
        value = redis_client.get(key)
        return value is not None

    @staticmethod
    def expire(key: str, ttl: int) -> None:
        redis_client.expire(key, ttl)

    @staticmethod
    def persist(key: str) -> None:
        redis_client.persist(key)

    @staticmethod
    def get_ttl(key: str) -> int:
        return redis_client.ttl(key)

    @staticmethod
    def __standalize(value: Any) -> str:
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value)
        else:
            return str(value)
