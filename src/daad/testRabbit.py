import asyncio
import os

import aio_pika
from dotenv import load_dotenv

from src.daad.constants import RABBITMQ_CONFIG
from src.daad.start import start_rabbitmq

load_dotenv()


def run():
    start_rabbitmq()

    async def main():
        # Create a connection to RabbitMQ
        # connection = await aio_pika.connect_robust(
        #     f"amqp://{RABBITMQ_CONFIG['user']}:{RABBITMQ_CONFIG['password']}@{RABBITMQ_CONFIG['host']}:{RABBITMQ_CONFIG['port']}/"
        # )
        connection = await aio_pika.connect_robust(os.environ.get("RABBITMQ_URL"))

        channel = await connection.channel()
        QUEUE_NAME = "test"
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        message = aio_pika.Message(body=b"Hello, RabbitMQ!")
        await channel.default_exchange.publish(message, routing_key=QUEUE_NAME)
        print(f" [x] Sent 'Hello, RabbitMQ!'")

        # Consume messages
        async def on_message(message: aio_pika.abc.AbstractIncomingMessage):
            async with message.process():
                print(f" [x] Received message: {message.body.decode()}")

        await queue.consume(on_message)

        await asyncio.Future()

    try:
        loop = asyncio.get_running_loop()  # Get the current event loop
    except RuntimeError:  # If no loop exists, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # Run the main function
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


# Run the main function
if __name__ == "__main__":
    run()
