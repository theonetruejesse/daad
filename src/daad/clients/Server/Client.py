import asyncio

import uvicorn

from src.daad.clients.AppClient import AppClient
from src.daad.clients.Server.AppServer import AppServer
from src.daad.constants import PORT


class ServerClient(AppClient):
    async def _setup(self):
        if self.client is not None:
            return self.client

        app = AppServer()
        config = uvicorn.Config(app(), host="0.0.0.0", port=PORT)
        server = uvicorn.Server(config)
        self.client = server
        await server.serve()
        return self.client

    async def cleanup(self):
        if self.server:
            print("Shutting down server...")
            self.server.should_exit = True
            try:
                await asyncio.wait_for(self.server.shutdown(), timeout=5.0)
            except asyncio.TimeoutError:
                print("Server shutdown timed out")

            # Force cleanup any remaining server tasks
            if hasattr(self.server, "servers"):
                for server in self.server.servers:
                    server.close()
                    await server.wait_closed()
