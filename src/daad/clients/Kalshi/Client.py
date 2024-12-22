import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.daad.clients.AppClient import AppClient
from src.daad.clients.Kalshi.Exchange import KalshiExchange
from src.daad.helpers import get_file_path


class KalshiClient(AppClient, KalshiExchange):
    def __init__(self):
        AppClient.__init__(self)
        self.client = None
        self.key_id = None
        self.private_key = None
        self.exchange_url = "/exchange"
        self.markets_url = "/markets"
        self.events_url = "/events"
        self.series_url = "/series"
        self.portfolio_url = "/portfolio"

    async def _setup(self):
        if self.client is not None:
            return self.client

        self.private_key = self._load_private_key_from_env("KALSHI_PK")
        self.key_id = os.getenv("KALSHI_KEY_ID")
        prod_api_base = "https://api.elections.kalshi.com/trade-api/v2"

        # Initialize the KalshiExchange part
        KalshiExchange.__init__(
            self,
            exchange_api_base=prod_api_base,
            key_id=self.key_id,
            private_key=self.private_key,
            cache_session=get_file_path("kalshi_cache"),
        )

        self.client = self
        self.warm_up_cache()
        return self.client

    def _load_private_key_from_env(self, env_var_name):
        encoded_key = os.getenv(env_var_name)
        if not encoded_key:
            raise ValueError(
                f"Environment variable '{env_var_name}' is not set or is empty."
            )
        key_data = base64.b64decode(encoded_key)
        private_key = serialization.load_pem_private_key(
            key_data,
            password=None,
            backend=default_backend(),
        )
        return private_key

    def get_client(self):
        return self.client
