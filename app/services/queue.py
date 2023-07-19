import logging
from typing import Callable

from aio_pika import ExchangeType, Message, connect

from app.core.singleton import singleton

logger = logging.getLogger(__name__)


@singleton
class QueueService():
    def __init__(self):
        self.amqp_url = "amqp://guest:guest@rabbitmq"
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect(self.amqp_url)
        self.channel = await self.connection.channel()
        logger.info("Connected to RabbitMQ")

    async def close(self):
        await self.connection.close()
        logger.info("Disconnected from RabbitMQ")

    async def publish_message(self, message: str, routing_key: str):
        # await self.channel.default_exchange.publish(
        #     Message(message.encode()),
        #     routing_key=routing_key
        # )
        exchange_name = 'fanout_exchange'
        exchange = await self.channel.declare_exchange(
            exchange_name, ExchangeType.FANOUT)
        await exchange.publish(
            Message(body=message.encode()),
            routing_key=''
        )
        logger.info("Message published")

    async def consume_messages(self, queue_name: str, callback: Callable):
        exchange_name = 'fanout_exchange'
        exchange = await self.channel.declare_exchange(
            exchange_name, ExchangeType.FANOUT)
        queue = await self.channel.declare_queue(queue_name)
        await queue.bind(exchange)  # Bind the queue to the fanout exchange
        await queue.consume(callback)
        logger.info("Message consumed")
