import aio_pika
from fastapi import APIRouter, BackgroundTasks, status

from app.models.schemas.health import Health
from app.services.cache import CacheService
from app.services.queue import QueueService

router = APIRouter()
cache_service = CacheService()
queue_service = QueueService()


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


@router.post("/produce")
async def produce(message: str):
    await queue_service.publish_message(message, routing_key='')
    return {"message": "Message published"}


async def consume_callback(message: aio_pika.IncomingMessage):
    async with message.process():
        # Retrieve the message body
        body = message.body.decode()
        # Process the message as needed
        print("Received message:", body)


@router.get("/consume")
async def consume():
    await queue_service.consume_messages('', callback=consume_callback)
    return {"message": "Consuming finished"}
