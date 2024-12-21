import os

__prod__ = os.getenv("ENVIRONMENT") == "production"
