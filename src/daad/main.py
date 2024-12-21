import asyncio

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.daad.services.setup import setup_api_server, setup_discord_client

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


def run():
    print("Dasein says hello!")

    async def main():
        # Start the Discord client
        await setup_discord_client()
        await setup_api_server()

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
