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

    async def cleanup(self):
        if self.client:
            print("Shutting down server...")
            self.client.should_exit = True
            try:
                await asyncio.wait_for(self.client.shutdown(), timeout=5.0)
            except asyncio.TimeoutError:
                print("Server shutdown timed out")

            # Force cleanup any remaining server tasks
            if hasattr(self.client, "servers"):
                for server in self.client.servers:
                    server.close()
                    await server.wait_closed()
