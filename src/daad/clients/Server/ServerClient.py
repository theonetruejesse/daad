import asyncio

import uvicorn

from src.daad.clients.AppClient import AppClient
from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient
from src.daad.clients.Server.Router import ServerRouter
from src.daad.constants import PORT


class ServerClient(ServerRouter, AppClient):
    def __init__(self):
        ServerRouter.__init__(self)

    async def _setup(self):
        config = uvicorn.Config(self.get_app(), host="0.0.0.0", port=PORT)
        server = uvicorn.Server(config)
        asyncio.create_task(server.serve())

    async def send_discord_message(self, channel_id: int, content: str):
        # Get RabbitMQ singleton instance
        rabbitmq = await RabbitMQClient.instance()

        # Format: "channel_id:content"
        message = f"{channel_id}:{content}"
        await rabbitmq.publish(routing_key="discord.notifications", message=message)
