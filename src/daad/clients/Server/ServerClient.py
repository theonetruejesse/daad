import asyncio

import uvicorn

from src.daad.clients.AppClient import AppClient
from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient
from src.daad.clients.Server.Router import ServerRouter
from src.daad.constants import PORT


class ServerClient(ServerRouter, AppClient):
    def __init__(self):
        self.rabbitmq: RabbitMQClient | None = None
        ServerRouter.__init__(self)

    async def _setup(self):
        """Initialize the FastAPI server and RabbitMQ connection"""
        # Initialize RabbitMQ first
        self.rabbitmq = await RabbitMQClient.instance()

        # Setup FastAPI server
        config = uvicorn.Config(
            self.get_app(), host="0.0.0.0", port=PORT, loop="asyncio"
        )
        server = uvicorn.Server(config)
        self.server_task = asyncio.create_task(server.serve())

        print(f"Server started on port {PORT}")

    async def publish_discord_message(self, channel_id: int, content: str):
        """Publish a message to Discord through RabbitMQ"""
        if not self.rabbitmq:
            self.rabbitmq = await RabbitMQClient.instance()

        message = f"{channel_id}:{content}"
        await self.rabbitmq.publish(
            routing_key="discord.notifications", message=message
        )
        print(f"Published Discord message: {message}")

    async def cleanup(self):
        """Cleanup server resources"""
        if hasattr(self, "server_task") and not self.server_task.done():
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass
