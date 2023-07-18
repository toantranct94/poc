import redis
# Redis connection parameters
from typing import Any


redis_host = 'redis'
redis_port = 6379
redis_password = None  # If your Redis instance has a password, provide it here
redis_db = 0

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    db=redis_db
)


class CacheService():

    def get(self, key: str) -> Any:
        return redis_client.get(key)

    def set_cache(self, key: str, value: Any) -> None:
        redis_client.set(key, value)
