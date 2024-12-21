from fastapi import FastAPI


class AppServer:
    def __init__(self):
        self.app = FastAPI()
        self.routes()

    def routes(self):
        @self.app.get("/hello")
        async def hello():
            return {"message": "Hello, World!"}

    def __call__(self):
        return self.app


# @API.get("/message")
# async def message():
#     discord_client = await setup_discord_client()
#     discord_client.send_message_to_channel(1320122496363532310, "Hello, World!")
#     return {"message": "Discord message sent"}
