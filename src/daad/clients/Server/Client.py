import asyncio

import uvicorn

from src.daad.clients.AppClient import AppClient
from src.daad.clients.Server.AppServer import AppServer
from src.daad.constants import PORT


class ServerClient(AppClient, AppServer):
    def __init__(self):
        AppClient.__init__(self)
        self.client = None

    async def _setup(self):
        if self.client is not None:
            return self.client

        # Initialize the AppServer part
        AppServer.__init__(self)

        config = uvicorn.Config(self.get_app(), host="0.0.0.0", port=PORT)
        self.client = uvicorn.Server(config)

        # Start server in a separate task to avoid blocking
        asyncio.create_task(self.client.serve())
        return self.client
