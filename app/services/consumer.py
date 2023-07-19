import asyncio
from aio_pika import connect, ExchangeType


async def consume_fanout():
    connection = await connect()
    channel = await connection.channel()

    exchange_name = 'fanout_exchange'
    queue_name = ''

    exchange = await channel.declare_exchange(exchange_name, ExchangeType.FANOUT)
    queue = await channel.declare_queue(queue_name)

    await queue.bind(exchange)  # Bind the queue to the fanout exchange

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = message.body.decode()
                print(f"Received message: {body}")

    await connection.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_fanout())
