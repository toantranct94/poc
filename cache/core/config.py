from pydantic import BaseSettings


class Settings(BaseSettings):
    # rabbitmq
    amqp_url: str = "amqp://guest:guest@rabbitmq"

    # redis
    redis_host: str = "redis"
    redis_port: str = 6379
    redis_password: str = None
    redis_db: int = 0
    default_cache_ttl: int = 3600


settings = Settings()
