import asyncio
import subprocess

from dotenv import load_dotenv

from src.daad.clients.Discord.Client import DiscordClient
from src.daad.clients.Server.Client import ServerClient
from src.daad.constants import __prod__
from src.daad.helpers import get_file_path

# Load environment variables
load_dotenv()


def run():
    print("Dasein says hello!\n")

    if not __prod__:
        # starts rabbitmq on local machine
        subprocess.run(["bash", get_file_path("start_rabbitmq.sh")], check=True)

    async def main():
        clients = []
        try:
            # Start clients concurrently
            clients = await asyncio.gather(
                DiscordClient.instance(), ServerClient.instance()
            )

            # Keep the program running
            await asyncio.Future()  # run forever
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
        finally:
            # Run cleanup with timeout
            print("Running cleanup...")
            try:
                await asyncio.wait_for(
                    asyncio.gather(*(client.cleanup() for client in clients)),
                    timeout=10.0,
                )
            except asyncio.TimeoutError:
                print("Cleanup timed out, forcing exit...")
            finally:
                print("Cleanup complete")

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
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    run()
