from fastapi import FastAPI

from src.daad.services.setup import setup_discord_client

API = FastAPI()


@API.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


@API.get("/message")
async def message():
    discord_client = await setup_discord_client()
    discord_client.send_message_to_channel(1320122496363532310, "Hello, World!")
    return {"message": "Discord message sent"}
