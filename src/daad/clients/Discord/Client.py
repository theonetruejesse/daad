import asyncio
import os

import discord

from src.daad.clients.AppClient import AppClient
from src.daad.clients.Discord.Bot import DiscordBot


class DiscordClient(DiscordBot, AppClient):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        DiscordBot.__init__(self, intents=intents)

    async def _setup(self):
        await self.login(os.getenv("DISCORD_TOKEN"))
        asyncio.create_task(self.connect())

    async def send_message_to_channel(self, channel_id: int, content: str):
        channel = self.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found.")
            return

        await channel.send(content)
