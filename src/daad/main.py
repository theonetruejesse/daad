import asyncio

from dotenv import load_dotenv

from src.daad.clients.Discord.Client import DiscordClient
from src.daad.clients.Server.Client import ServerClient

# Load environment variables
load_dotenv()


def run():
    print("Dasein says hello!")

    async def main():
        await DiscordClient.instance()
        await ServerClient.instance()

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
