import os
import subprocess

import redis.asyncio as redis

from src.daad.clients.AppClient import AppClient
from src.daad.constants import IS_TESTING_REDIS_PROD, LOCAL_REDIS_CONFIG, __prod__
from src.daad.helpers import get_file_path


class RedisClient(AppClient):
    """
    Singleton client for Redis operations.
    """

    def __init__(self):
        self.redis = None

    """Redis Client Setup"""

    async def _setup(self):
        if not __prod__ and not IS_TESTING_REDIS_PROD:
            self._start_local_redis()

        try:
            connection_url = self._get_connection_string()
            self.redis = await redis.from_url(connection_url)
            await self.redis.ping()
            print("Connected to Redis successfully")
        except Exception as e:
            print(f"Error connecting to Redis: {str(e)}")
            raise e

    def _start_local_redis(self):
        """Start local Redis server for development"""
        env = os.environ.copy()
        env.update(LOCAL_REDIS_CONFIG)
        subprocess.run(["bash", get_file_path("start_redis.sh")], env=env, check=True)

    def _get_connection_string(self):
        """Get appropriate connection string based on environment"""
        if __prod__:
            return os.getenv("REDIS_URL")
        elif IS_TESTING_REDIS_PROD:
            return os.getenv("REDIS_PUBLIC_URL")
        else:
            config = LOCAL_REDIS_CONFIG
            return f"redis://{config['REDIS_HOST']}:{config['REDIS_PORT']}"

    async def cleanup(self):
        """Cleanup resources on shutdown"""
        if self.redis:
            try:
                await self.redis.close()
            except Exception as e:
                print(f"Error closing Redis connection: {str(e)}")
        print("RedisClient cleanup complete")

    def _channel_connect_exception(self):
        return Exception("Channel not connected")
