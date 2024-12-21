import os

__prod__ = os.getenv("ENVIRONMENT") == "production"

PORT = 8000

APP_URL = (
    f"http://localhost:{PORT}" if not __prod__ else "daad-production.up.railway.app"
)
