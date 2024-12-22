import os

__prod__ = os.getenv("RAILWAY_ENVIRONMENT_NAME") == "production"

PORT = 8000

APP_URL = f"http://localhost:{PORT}" if not __prod__ else os.getenv("APP_URL")

# Discord Channel IDs

TESTING_CHANNELS = [1317656187646513185]
DAILY_LOG_CHANNEL = 1320122496363532310
