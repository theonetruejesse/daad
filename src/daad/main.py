from dotenv import load_dotenv

from src.daad.clients.setup import setup_discord_client

load_dotenv()


def run():
    print("Dasein says hello!")
    setup_discord_client()


if __name__ == "__main__":
    run()
