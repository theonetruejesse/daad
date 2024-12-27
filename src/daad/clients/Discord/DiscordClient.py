import asyncio
import os

import aio_pika
import discord

from src.daad.clients.AppClient import AppClient
from src.daad.clients.Discord.Bot import DiscordBot
from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient


class DiscordClient(DiscordBot, AppClient):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.rabbitmq: RabbitMQClient | None = None
        DiscordBot.__init__(self, intents=intents)

    async def _setup(self):
        """Initialize Discord connection and setup RabbitMQ consumer"""
        # Setup Discord
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("DISCORD_TOKEN environment variable not set")

        await self.login(token)

        # Start Discord connection in background
        self.discord_task = asyncio.create_task(self.connect())

        # Setup RabbitMQ consumer
        self.rabbitmq = await RabbitMQClient.instance()
        await self.setup_message_consumer()

    async def setup_message_consumer(self):
        """Setup RabbitMQ consumer for Discord notifications"""
        await self.rabbitmq.subscribe(
            queue_name="discord_notifications",
            routing_key="discord.notifications",
            callback=self._handle_rabbitmq_message,
        )

    async def _handle_rabbitmq_message(self, message: aio_pika.Message):
        """Handle incoming RabbitMQ messages"""
        try:
            # Decode message content
            content = message.body.decode()
            channel_id, message_content = content.split(":", 1)

            # Send to Discord channel
            await self.send_message_to_channel(
                channel_id=int(channel_id), content=message_content
            )

            # Acknowledge message
            await message.ack()
        except ValueError as e:
            print(f"Invalid message format received: {content}")
            # Still ack the message to remove it from queue
            await message.ack()
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            # Reject the message and requeue it
            await message.reject(requeue=True)

    async def send_message_to_channel(self, channel_id: int, content: str):
        channel = self.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found.")
            return
        await channel.send(content)

    async def cleanup(self):
        """Cleanup resources on shutdown"""
        # Close Discord connection
        await self.close()

        # Cancel Discord connection task
        if hasattr(self, "discord_task"):
            self.discord_task.cancel()
            try:
                await self.discord_task
            except asyncio.CancelledError:
                pass

        # Cleanup RabbitMQ
        if self.rabbitmq:
            await self.rabbitmq.cleanup()
