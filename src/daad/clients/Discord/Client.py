import asyncio
import os

import discord

from src.daad.clients.Discord import Discord
from src.daad.clients.utils.AppClient import AppClient


@AppClient
class DiscordClient:
    async def _setup(self):
        if self.client is not None:
            return self.client

        intents = discord.Intents.default()
        intents.message_content = True
        client = Discord(intents=intents)

        # Log in the client
        await client.login(os.getenv("DISCORD_TOKEN"))
        # Connect in a separate task to avoid blocking
        asyncio.create_task(client.connect())

        self.client = client
        return self.client

    def get_client(self):
        if self.client is None:
            self._setup()

        return self.client
