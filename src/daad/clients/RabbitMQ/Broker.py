import asyncio

import aio_pika


class RabbitMQBroker:
    def __init__(self, channel):
        self.channel: aio_pika.Channel = channel
        self.exchange_name = "app_exchange"
        self.exchange: aio_pika.Exchange | None = None
        self._consuming_tasks: set[asyncio.Task] = set()

    async def setup_exchange(self):
        try:
            # First try to delete the exchange if it exists
            await self.channel.exchange_delete(self.exchange_name)
        except Exception:
            pass  # Ignore if exchange doesn't exist

        self.exchange = await self.channel.declare_exchange(
            self.exchange_name, type="topic", durable=True
        )

    async def publish(self, routing_key: str, message: str):
        """
        Publish a message to the exchange with the given routing key.

        Args:
            routing_key (str): The routing key for message delivery
            message (str): The message content to publish
        """
        if not self.channel:
            raise self._channel_connect_exception()
        if not self.exchange:
            await self.setup_exchange()

        await self.exchange.publish(
            message=aio_pika.Message(body=message.encode()), routing_key=routing_key
        )
        print(f"Published message: {message} with routing_key: {routing_key}")

    async def subscribe(self, queue_name: str, routing_key: str, callback):
        """
        Sets up a queue and starts consuming messages from it.
        Will delete and recreate the queue if properties don't match.
        """
        if not self.channel:
            raise self._channel_connect_exception()
        if not self.exchange:
            await self.setup_exchange()

        # First try to delete the queue if it exists
        try:
            await self.channel.queue_delete(queue_name)
        except Exception:
            pass  # Ignore if queue doesn't exist

        # Declare queue
        queue = await self.channel.declare_queue(
            queue_name, durable=True, auto_delete=False
        )

        # Bind queue to exchange
        await queue.bind(exchange=self.exchange_name, routing_key=routing_key)

        print(f"Starting to consume messages from queue: {queue_name}")

        # Create and track the consuming task
        task = asyncio.create_task(self._consume_forever(queue, callback))
        self._consuming_tasks.add(task)
        task.add_done_callback(self._consuming_tasks.discard)

    async def _consume_forever(self, queue: aio_pika.Queue, callback):
        """
        Internal method to handle continuous message consumption.
        """
        try:
            await queue.consume(callback)
            # Keep the consumer running
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            print("Consumer task cancelled")
            raise
        except Exception as e:
            print(f"Error in consume task: {str(e)}")
            raise
        finally:
            try:
                await queue.close()
            except Exception:
                pass  # Ignore cleanup errors

    async def cleanup(self):
        """Cleanup all resources"""
        # Cancel all consuming tasks
        for task in self._consuming_tasks:
            if not task.done():
                task.cancel()

        # Wait for all tasks to complete
        if self._consuming_tasks:
            await asyncio.gather(*self._consuming_tasks, return_exceptions=True)

        # Cleanup channel
        if self.channel:
            try:
                await self.channel.close()
            except Exception:
                pass  # Ignore cleanup errors

    def _channel_connect_exception(self):
        return Exception("Channel not connected")
