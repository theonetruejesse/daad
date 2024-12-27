import os
import subprocess

import aio_pika

from src.daad.clients.AppClient import AppClient
from src.daad.clients.RabbitMQ.Broker import RabbitMQBroker
from src.daad.constants import IS_TESTING_RABBITMQ_PROD, LOCAL_RABBITMQ_CONFIG, __prod__
from src.daad.helpers import get_file_path


class RabbitMQClient(AppClient):
    """
    Singleton client for RabbitMQ operations.
    Handles connection management and provides high-level messaging pub/sub operations.
    """

    def __init__(self):
        # can't inherit broker directly because of metaclass conflict:
        # the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
        self.broker: RabbitMQBroker | None = None
        self.connection = None

    async def _setup(self):
        """Initialize RabbitMQ connection, channel, and setup broker"""
        if not __prod__ and not IS_TESTING_RABBITMQ_PROD:
            self._start_local_rabbitmq()

        self.connection = await aio_pika.connect_robust(self._get_connection_string())
        channel = await self.connection.channel()

        self.broker = RabbitMQBroker(channel)
        await self.broker.setup_exchange()
        print(f"RabbitMQClient connected to broker channel: {self.broker.channel}")

    def _start_local_rabbitmq(self):
        """Start local RabbitMQ server for development"""
        env = os.environ.copy()
        env.update(LOCAL_RABBITMQ_CONFIG)
        subprocess.run(
            ["bash", get_file_path("start_rabbitmq.sh")], env=env, check=True
        )

    def _get_connection_string(self):
        """Get appropriate RabbitMQ connection string based on environment"""
        if __prod__:
            return os.getenv("RABBITMQ_PRIVATE_URL")
        elif IS_TESTING_RABBITMQ_PROD:
            return os.getenv("RABBITMQ_URL")
        else:
            config = LOCAL_RABBITMQ_CONFIG
            return f"amqp://{config['RABBITMQ_USER']}:{config['RABBITMQ_PASS']}@{config['RABBITMQ_HOST']}:{config['RABBITMQ_PORT']}/"

    async def cleanup(self):
        """Cleanup resources on shutdown"""
        if self.broker.channel:
            await self.broker.channel.close()
        if self.connection:
            await self.connection.close()
        await self.broker.cleanup()

    def _channel_connect_exception(self):
        return Exception("Channel not connected")

    """Broker Bindings"""

    async def publish(self, routing_key: str, message: str):
        """Publish a message to a specific routing key"""
        await self.broker.publish(routing_key, message)

    async def subscribe(self, queue_name: str, routing_key: str, callback):
        """Start consuming messages from a queue with specified routing key"""
        await self.broker.subscribe(queue_name, routing_key, callback)
