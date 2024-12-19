import os

import discord
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

from src.daad.clients.Discord import DiscordClient
from src.daad.clients.Kalshi import ExchangeClient
from src.daad.utils.helpers import get_file_path

load_dotenv()


def setup_discord_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordClient(intents=intents)

    client.run(os.getenv("DISCORD_TOKEN"))
    return client


def setup_exchange_client():
    """
    Initialize the Kalshi ExchangeClient.
    """

    def load_private_key_from_file(file_name):
        with open(get_file_path(file_name), "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,  # or provide a password if your key is encrypted
                backend=default_backend(),
            )
        return private_key

    # configs
    prod_private_key = load_private_key_from_file("kalshi-pk.key")
    prod_key_id = os.getenv("KALSHI_KEY_ID")
    prod_api_base = "https://api.elections.kalshi.com/trade-api/v2"

    return ExchangeClient.instance(
        exchange_api_base=prod_api_base,
        key_id=prod_key_id,
        private_key=prod_private_key,
        cache_session=get_file_path("kalshi_cache"),
    )
