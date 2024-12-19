import discord


class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: discord.Message):
        if message.author == self.user and not self.user.mentioned_in(message):
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
