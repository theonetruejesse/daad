import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.daad.clients.Kalshi.Exchange import KalshiExchange
from src.daad.clients.utils.AppClient import AppClient
from src.daad.clients.utils.helpers import get_file_path


@AppClient
class KalshiClient:
    def get_client(self):
        if self.client is None:
            self._setup()
        return self.client

    async def _setup(self):
        if self.client is not None:
            return self.client

        prod_private_key = self._load_private_key_from_env("KALSHI_PK")
        prod_key_id = os.getenv("KALSHI_KEY_ID")
        prod_api_base = "https://api.elections.kalshi.com/trade-api/v2"

        self.client = KalshiExchange.instance(
            exchange_api_base=prod_api_base,
            key_id=prod_key_id,
            private_key=prod_private_key,
            cache_session=get_file_path("kalshi_cache"),
        )
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
