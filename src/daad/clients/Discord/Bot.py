import discord

from src.daad.constants import TESTING_CHANNELS, __prod__


class DiscordBot(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: discord.Message):
        if (
            message.author == self.user  # ignore messages from the bot itself
            or not self.user.mentioned_in(message)  # only when bot is pinged
            or not self._is_valid_channel(message)  # prevents duplicate messages
        ):
            return

        print(message)
        await message.channel.send(f"Hello {message.author}!")

    def _is_valid_channel(self, message: discord.Message):

        if not __prod__ and message.channel.id not in TESTING_CHANNELS:
            print(
                f"[DEBUG] Ignoring message in channel {message.channel.id} (not in TESTING_CHANNELS)"
            )
            return False
        elif __prod__ and message.channel.id in TESTING_CHANNELS:
            print(
                f"[DEBUG] Ignoring message in TESTING_CHANNELS during production: {message.channel.id}"
            )
            return False

        return True
