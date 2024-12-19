import discord


class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        print(message.channel)
        await message.channel.send(f"Hello {message.author}!")
