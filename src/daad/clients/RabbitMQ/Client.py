import os
import subprocess

import aio_pika

from src.daad.clients.AppClient import AppClient
from src.daad.clients.RabbitMQ.Broker import RabbitMQBroker
from src.daad.constants import RABBITMQ_CONFIG, TEST_RABBITMQ_PROD, __prod__
from src.daad.helpers import get_file_path


class RabbitMQClient(AppClient):
    def __init__(self):
        """
        can't inherit broker directly because of metaclass conflict:
        the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
        """
        self.broker = RabbitMQBroker()

    async def _setup(self):
        if not __prod__ and not TEST_RABBITMQ_PROD:
            self._start_local_rabbitmq()

        connection = await aio_pika.connect_robust(self._get_connection_string())
        self.broker.channel = await connection.channel()
        print(f"RabbitMQClient connected to broker channel: {self.broker.channel}")

    def _start_local_rabbitmq(self):
        env = os.environ.copy()
        env.update(
            {
                "RABBITMQ_DEFAULT_USER": RABBITMQ_CONFIG["user"],
                "RABBITMQ_DEFAULT_PASS": RABBITMQ_CONFIG["password"],
                "RABBITMQ_PORT": RABBITMQ_CONFIG["port"],
                "RABBITMQ_MANAGEMENT_PORT": RABBITMQ_CONFIG["management_port"],
            }
        )
        subprocess.run(
            ["bash", get_file_path("start_rabbitmq.sh")], env=env, check=True
        )

    def _get_connection_string(self):
        if __prod__:
            return os.getenv("RABBITMQ_URL")
        else:
            return f"amqp://{RABBITMQ_CONFIG['user']}:{RABBITMQ_CONFIG['password']}@{RABBITMQ_CONFIG['host']}:{RABBITMQ_CONFIG['port']}/"

    """ Broker Bindings """

    async def publish(self, routing_key: str, message: str):
        await self.broker.publish(routing_key, message)

    async def consume(self, queue_name: str, routing_key: str, callback):
        await self.broker.consume(queue_name, routing_key, callback)

    async def start_consuming(self, queue_name: str, routing_key: str, callback):
        await self.broker.start_consuming(queue_name, routing_key, callback)
