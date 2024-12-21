import asyncio
import base64
import os

import discord
import uvicorn
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.daad.services.api import API
from src.daad.services.Discord import DiscordClient
from src.daad.services.Kalshi import ExchangeClient
from src.daad.services.utils.helpers import get_file_path

_discord_client = None


async def setup_discord_client():
    """
    Initialize the Discord client.
    """
    global _discord_client

    if _discord_client is not None:
        return _discord_client

    print("Setting up Discord client")

    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordClient(intents=intents)

    _discord_client = client

    # Log in the client
    await client.login(os.getenv("DISCORD_TOKEN"))
    # Connect in a separate task to avoid blocking
    asyncio.create_task(client.connect())

    print("Discord client setup complete")
    return _discord_client


async def setup_api_server():
    config = uvicorn.Config(API, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


def setup_exchange_client():
    """
    Initialize the Kalshi ExchangeClient.
    """
    prod_private_key = load_private_key_from_env("KALSHI_PK")
    prod_key_id = os.getenv("KALSHI_KEY_ID")
    prod_api_base = "https://api.elections.kalshi.com/trade-api/v2"

    def load_private_key_from_env(env_var_name):
        encoded_key = os.getenv(env_var_name)
        if not encoded_key:
            raise ValueError(
                f"Environment variable '{env_var_name}' is not set or is empty."
            )
        key_data = base64.b64decode(encoded_key)
        private_key = serialization.load_pem_private_key(
            key_data,
            password=None,  # Or provide a password if your key is encrypted
            backend=default_backend(),
        )
        return private_key

    return ExchangeClient.instance(
        exchange_api_base=prod_api_base,
        key_id=prod_key_id,
        private_key=prod_private_key,
        cache_session=get_file_path("kalshi_cache"),
    )
