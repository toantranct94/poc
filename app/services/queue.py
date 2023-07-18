from logging import Logger

from aio_pika import Message, connect

from app.core.singleton import singleton

logger = Logger(__name__)


@singleton
class QueueService():
    def __init__(self):
        self.amqp_url = "amqp://guest:guest@localhost"
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect(self.amqp_url)
        self.channel = await self.connection.channel()
        logger.info("Connected to RabbitMQ")

    async def close(self):
        await self.connection.close()
        logger.info("Disconnected from RabbitMQ")

    async def publish_message(self, message, routing_key):
        await self.channel.default_exchange.publish(
            Message(message.encode()),
            routing_key=routing_key
        )
        logger.info("Message published")

    async def consume_messages(self, queue_name, callback):
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(callback)
        logger.info("Message consumed")
