import asyncio
import signal

from dotenv import load_dotenv

from src.daad.clients import AppClient
from src.daad.clients.Cron.CronClient import CronClient
from src.daad.clients.Discord.DiscordClient import DiscordClient
from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient
from src.daad.clients.Server.ServerClient import ServerClient

# Load environment variables
load_dotenv()


async def main():
    """Main application coroutine"""
    clients = []
    try:
        # Initialize clients concurrently
        clients = await asyncio.gather(
            RabbitMQClient.instance(),
            DiscordClient.instance(),
            ServerClient.instance(),
            CronClient.instance(),
        )

        # Create a shutdown event for signal handling
        shutdown_event = asyncio.Event()

        # Define signal handler to set shutdown event
        def handle_shutdown(*_):
            print("\nReceived shutdown signal...")
            shutdown_event.set()

        # Register signal handlers for graceful shutdown
        for sig in (signal.SIGINT, signal.SIGTERM):
            asyncio.get_running_loop().add_signal_handler(sig, handle_shutdown)

        await shutdown_event.wait()  # Wait until a shutdown signal is received

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise
    finally:
        if clients:
            print("\nRunning cleanup...")
            try:
                # Run cleanup with timeout
                await asyncio.wait_for(
                    asyncio.gather(
                        *(client.cleanup() for client in clients),
                        return_exceptions=True,
                    ),
                    timeout=10.0,
                )
                print("Cleanup complete")
            except asyncio.TimeoutError:
                print("Cleanup timed out, forcing exit...")
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")


def run():
    """Entry point function"""
    print("Dasein says hello!\n")

    # Setup event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Run main with proper signal handling
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt...")
    finally:
        try:
            # Clean shutdown of the event loop
            pending = asyncio.all_tasks(loop)
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        finally:
            loop.close()


if __name__ == "__main__":
    run()
