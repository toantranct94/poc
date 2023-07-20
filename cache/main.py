import asyncio
import json

from aio_pika import IncomingMessage

from cache.services.cache import CacheService
from cache.services.queue import QueueService

queue_service = QueueService()


async def on_message(message: IncomingMessage):
    message = message.body.decode("utf-8")
    message = json.loads(message)
    print(message)
    try:
        CacheService.insert(**message)
    except Exception as e:
        print(f"Failed to insert into Redis: {e}")
        message.nack(requeue=True)


async def main():
    await queue_service.connect()
    queue = await queue_service.channel.declare_queue("cache", exclusive=True)
    await queue.consume(on_message)


if __name__ == "__main__":
    print("Start listining...")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
