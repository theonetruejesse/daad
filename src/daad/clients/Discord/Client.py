import asyncio
import os

import discord

from src.daad.clients.Discord.Bot import DiscordBot
from src.daad.clients.utils.AppClient import AppClient


class DiscordClient(AppClient):
    async def _setup(self):
        if self.client is not None:
            return self.client

        intents = discord.Intents.default()
        intents.message_content = True
        client = DiscordBot(intents=intents)

        # Log in the client
        await client.login(os.getenv("DISCORD_TOKEN"))
        # Connect in a separate task to avoid blocking
        asyncio.create_task(client.connect())

        self.client = client
        return self.client

    async def send_message_to_channel(self, channel_id: int, content: str):
        channel = self.client.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found.")
            return

        await channel.send(content)
