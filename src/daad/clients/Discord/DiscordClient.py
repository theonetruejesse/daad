import asyncio
import os

import discord

from src.daad.clients.AppClient import AppClient
from src.daad.clients.Discord.Bot import DiscordBot
from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient


class DiscordClient(DiscordBot, AppClient):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        DiscordBot.__init__(self, intents=intents)

    async def _setup(self):
        await self.login(os.getenv("DISCORD_TOKEN"))
        asyncio.create_task(self.connect())

        # Get RabbitMQ singleton instance
        rabbitmq = await RabbitMQClient.instance()
        await rabbitmq.start_consuming(
            queue_name="discord_notifications",
            routing_key="discord.notifications",
            callback=self._handle_rabbitmq_message,
        )

    async def _handle_rabbitmq_message(self, message: str):
        try:
            channel_id, content = message.split(":", 1)
            await self.send_message_to_channel(int(channel_id), content)
        except ValueError:
            print(f"Invalid message format received: {message}")

    async def send_message_to_channel(self, channel_id: int, content: str):
        channel = self.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found.")
            return

        await channel.send(content)
