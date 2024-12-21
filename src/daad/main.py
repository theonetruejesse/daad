import asyncio

from dotenv import load_dotenv

from src.daad.clients.Discord.Client import DiscordClient
from src.daad.clients.Server.Client import ServerClient

# Load environment variables
load_dotenv()


def run():
    print("Dasein says hello!")

    async def main():
        # Start both clients concurrently
        await asyncio.gather(DiscordClient.instance(), ServerClient.instance())

        # Keep the program running
        try:
            await asyncio.Future()  # run forever
        except KeyboardInterrupt:
            # Graceful shutdown could be implemented here
            pass

    # Handle the event loop
    try:
        loop = asyncio.get_running_loop()  # Get the current event loop
    except RuntimeError:  # If no loop exists, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the main function
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()
    finally:
        loop.close()


if __name__ == "__main__":
    run()
