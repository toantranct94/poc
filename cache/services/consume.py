import asyncio
import json

from aio_pika import IncomingMessage, connect

from app.core.config import settings
from app.services.cache import CacheService


async def on_message(message: IncomingMessage):
    message = message.body.decode("utf-8")
    message = json.loads(message)
    print(message)
    try:
        CacheService.insert(**message)
    except Exception as e:
        print(f"Failed to insert into Redis: {e}")
        message.nack(requeue=True)


async def main(loop):
    connection = await connect(settings.amqp_url, loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue("cache", exclusive=True)

    await queue.consume(on_message)


if __name__ == "__main__":
    print("Start listining...")
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
