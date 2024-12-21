import os

__prod__ = os.getenv("environment") == "production"
