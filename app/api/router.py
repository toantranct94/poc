import json
import aio_pika
from fastapi import APIRouter, BackgroundTasks, status

from app.models.schemas.health import Health
from app.models.schemas.cache import Cache
from app.services.cache import CacheService
from app.services.queue import QueueService

router = APIRouter()
queue_service = QueueService()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=Health,
    tags=["Health Check"],
    summary="Check health",
    description="Endpoint to check the health of the API.",
)
def health():
    """
    Check heath
    """
    return Health()


@router.get(
    "/cache/{key}",
    status_code=status.HTTP_200_OK,
    response_model=Cache,
    tags=["Cache"],
    summary="Get cache by key",
    description="Endpoint to get cache data by key.",
)
async def get_cache(key: str):
    """
    Get cache by key
    """
    cache = Cache(key=key, value=None, ttl=None)
    redis_value = CacheService.get(key)
    if redis_value:
        cache.value = redis_value
        cache.ttl = CacheService.get_ttl(key)
    return cache


@router.post(
    "/cache",
    status_code=status.HTTP_200_OK,
    tags=["Cache"],
    summary="Update cache",
    description= """
    Update cache

    This endpoint allows you to update the cache with the provided data.

    Parameters:
        - key (str): The unique key for the cache.
        - value (Optional[Dict]): The data to be stored in the cache as a dictionary. (Default: None)
        - ttl (Optional[int]): The time to live for the cache data in seconds. Use -1 for indefinite (no expiration). (Default: None)

    Response:
        - 200 OK: Returns the updated cache data.

    Example Usage:
        ```
        {
            "key": "user_123",
            "value": {
                "name": "John",
                "age": 30
            },
            "ttl": -1
        }
        ```
    """,
)
async def update_cache(cache: Cache, background_tasks: BackgroundTasks):
    background_tasks.add_task(queue_service.publish_message, json.dumps(cache.dict()))
    return cache
