import json
import aio_pika
from fastapi import APIRouter, BackgroundTasks, status

from app.models.schemas.health import Health
from app.services.cache import CacheService
from app.services.queue import QueueService

router = APIRouter()
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
    sample code for get/set cache with redis and rabbitmq
     - key: redis key
     - value: any
    """
    key = "redis"
    item = {
        "key": key,
        "value": {}
    }
    value = CacheService.get(key)
    if value is None:
        item.update({
            "value": {
                "v": 1
            }
        })
        background_tasks.add_task(
            queue_service.publish_message, json.dumps(item))
        item.update({
            'from': 'raw'
        })
        return item
    item.update({
        'value': value,
        'from': 'redis'
    })
    return item


@router.post("/produce")
async def produce(message: str):
    await queue_service.publish_message(message, routing_key='cache')
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
