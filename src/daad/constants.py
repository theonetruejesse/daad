import os

__prod__ = os.getenv("RAILWAY_ENVIRONMENT_NAME") == "production"

PORT = 8000

APP_URL = f"http://localhost:{PORT}" if not __prod__ else os.getenv("APP_URL")

# Discord Channel IDs

TESTING_CHANNELS = [1317656187646513185]
DAILY_LOG_CHANNEL = 1320122496363532310

# RabbitMQ credentials

IS_TEST_RABBITMQ_PROD = False  # change this for when testing connections

LOCAL_RABBITMQ_CONFIG = {
    "user": "guest",
    "password": "guest",
    "host": "localhost",
    "port": "5672",
    "management_port": "15672",
}
