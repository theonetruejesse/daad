import asyncio
import base64
import os

import discord
import uvicorn
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

from src.daad.services.api import API
from src.daad.services.Discord import DiscordClient
from src.daad.services.Kalshi import ExchangeClient
from src.daad.utils.helpers import get_file_path


async def setup_api_server():
    config = uvicorn.Config(API, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


discord_client = None


async def setup_discord_client():
    global discord_client

    if discord_client is not None:
        return discord_client

    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordClient(intents=intents)

    discord_client = client  # Set the global client before starting it

    # Log in the client
    await client.login(os.getenv("DISCORD_TOKEN"))
    # Connect in a separate task to avoid blocking
    asyncio.create_task(client.connect())

    return discord_client


def setup_exchange_client():
    """
    Initialize the Kalshi ExchangeClient.
    """

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

    # configs
    prod_private_key = load_private_key_from_env("KALSHI_PK")
    prod_key_id = os.getenv("KALSHI_KEY_ID")
    prod_api_base = "https://api.elections.kalshi.com/trade-api/v2"

    return ExchangeClient.instance(
        exchange_api_base=prod_api_base,
        key_id=prod_key_id,
        private_key=prod_private_key,
        cache_session=get_file_path("kalshi_cache"),
    )
