import asyncio

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.daad.clients.setup import setup_discord_client

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()


# # Define your FastAPI endpoints
# @app.post("/send-message")
# async def send_message(channel_id: int, message: str):
#     """
#     Endpoint to send a message to a specific Discord channel.
#     """
#     discord_client = setup_discord_client()  # Ensure this sets up your bot correctly
#     channel = discord_client.get_channel(channel_id)
#     if channel:
#         await channel.send(message)
#         return {"status": "success", "message": f"Message sent to channel {channel_id}"}
#     else:
#         return {"status": "error", "message": "Channel not found"}


@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


# async def start_services():
#     # Start the Discord bot
#     await setup_discord_client()

#     # Start the FastAPI server
#     config = uvicorn.Config(app, host="0.0.0.0", port=8000)
#     server = uvicorn.Server(config)
#     await server.serve()


def run():
    print("Dasein says hello!")

    async def main():
        # Start the Discord client
        await setup_discord_client()

        # Run the FastAPI server
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()

    # Handle the event loop
    try:
        loop = asyncio.get_running_loop()  # Get the current event loop
    except RuntimeError:  # If no loop exists, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the main function
    loop.run_until_complete(main())


if __name__ == "__main__":
    run()
