import os

import discord


class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: discord.Message):
        if (
            message.author == self.user  # ignore messages from the bot itself
            or not self.user.mentioned_in(message)  # only when bot is pinged
            or not self.is_valid_channel(message)  # prevents duplicate messages
        ):
            return

        print(message)
        await message.channel.send(f"Hello {message.author}!")

    # channel_ids across Discord are globally unique
    async def send_message_to_channel(self, channel_id: int, content: str):
        channel = self.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found.")
            return

        await channel.send(content)

    def is_valid_channel(message: discord.Message):
        TESTING_CHANNELS = [1317656187646513185]
        environment = os.getenv("environment")

        if environment != "production" and message.channel.id not in TESTING_CHANNELS:
            return False
        elif environment == "production" and message.channel.id in TESTING_CHANNELS:
            return False

        return True
