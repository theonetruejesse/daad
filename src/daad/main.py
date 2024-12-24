import asyncio

from dotenv import load_dotenv

from src.daad.clients.Discord.DiscordClient import DiscordClient
from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient
from src.daad.clients.Server.ServerClient import ServerClient
from src.daad.constants import __prod__

# Load environment variables
load_dotenv()


def run():
    print("Dasein says hello!\n")

    async def main():
        try:
            # Initialize RabbitMQ first since others depend on it
            rabbitmq = await RabbitMQClient.instance()

            # Initialize other clients concurrently
            discord, server = await asyncio.gather(
                DiscordClient.instance(), ServerClient.instance()
            )

            # Store all clients for cleanup
            clients = [rabbitmq, discord, server]

            # Keep the program running forever
            await asyncio.Future()

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
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    run()
