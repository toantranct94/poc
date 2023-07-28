import asyncio
import json
import logging

from aio_pika import IncomingMessage

from cache.services.cache import CacheService
from cache.services.queue import QueueService

queue_service = QueueService()

logging.basicConfig(level=logging.INFO)  # Set the logging level to DEBUG


async def on_message(message: IncomingMessage):
    message = message.body.decode("utf-8")
    message = json.loads(message)
    logging.info(message)  # Use logging.debug() instead of print()
    try:
        CacheService.set(**message)
    except Exception as e:
        logging.error(f"Failed to insert into Redis: {e}")
        message.nack(requeue=True)


async def main():
    await queue_service.connect()
    queue = await queue_service.channel.declare_queue("cache", exclusive=True)
    await queue.consume(on_message)

if __name__ == "__main__":
    logging.info("Start listening...")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
