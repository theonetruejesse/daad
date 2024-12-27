import os

__prod__ = os.getenv("RAILWAY_ENVIRONMENT_NAME") == "production"

PORT = 8000

APP_URL = f"http://localhost:{PORT}" if not __prod__ else os.getenv("APP_URL")

# Discord Channel IDs

TESTING_CHANNELS = [1317656187646513185]
DAILY_LOG_CHANNEL = 1320122496363532310

# RabbitMQ credentials

IS_TESTING_RABBITMQ_PROD = False  # change this for when testing connections

LOCAL_RABBITMQ_CONFIG = {
    "RABBITMQ_USER": "guest",
    "RABBITMQ_PASS": "guest",
    "RABBITMQ_HOST": "localhost",
    "RABBITMQ_PORT": "5672",
    "RABBITMQ_MANAGEMENT_PORT": "15672",
}
