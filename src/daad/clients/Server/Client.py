import uvicorn

from src.daad.clients.Server.AppServer import AppServer
from src.daad.clients.utils.AppClient import AppClient


@AppClient
class ServerClient:
    def get_client(self):
        if self.client is None:
            self._setup()

        return self.client

    async def _setup(self):
        if self.client is not None:
            return self.client

        app = AppServer()

        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        self.client = server
        await server.serve()
        return self.client
