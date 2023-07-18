from fastapi import APIRouter, BackgroundTasks, status

from app.models.schemas.health import Health
from app.services.cache import CacheService

router = APIRouter()
cache_service = CacheService()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=Health,
)
def health():
    """
    Check heath
    """
    return Health()


@router.get(
    "/redis",
    status_code=status.HTTP_200_OK,
)
async def update(
    background_tasks: BackgroundTasks,
):
    """
    Check heath
    """
    key = "test"
    value = cache_service.get(key)
    if value is None:
        background_tasks.add_task(cache_service.set_cache, key, "test")
        return {"key": key, "value": "test", "from": "raw"}
    return {"key": key, "value": value.decode(), "from": "redis"}
