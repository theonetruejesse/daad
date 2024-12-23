import asyncio


class RabbitMQBroker:
    def __init__(self):
        self.channel = None
        self.exchange = "default"

    async def publish(self, routing_key: str, message: str):
        if not self.channel:
            raise self._channel_connect_exception()
        await self.channel.basic_publish(
            exchange=self.exchange, routing_key=routing_key, body=message.encode()
        )
        print(f"Published message: {message} with routing_key: {routing_key}")

    async def start_consuming(self, queue_name: str, routing_key: str, callback):
        asyncio.create_task(self._consume_task(queue_name, routing_key, callback))

    async def _consume_task(self, queue_name: str, routing_key: str, callback):
        await self.consume(
            queue_name=queue_name, routing_key=routing_key, callback=callback
        )
        try:
            print(f"Starting to consume messages from queue: {queue_name}")
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("Stopped consuming")
            await self.channel.close()

    async def consume(self, queue_name: str, routing_key: str, callback):
        if not self.channel:
            raise self._channel_connect_exception()
        queue = await self.channel.declare_queue(queue_name)
        await queue.bind(exchange=self.exchange, routing_key=routing_key)
        print(f"Waiting for messages on queue: {queue_name}")
        await queue.consume(callback)

    def _channel_connect_exception(self):
        return Exception("RabbitMQ channel is not initialized. Call connect() first.")
