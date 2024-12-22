import asyncio

import aio_pika
import aiohttp


class RabbitMQClient:
    _instance = None

    @classmethod
    async def instance(cls):
        if cls._instance is None:
            cls._instance = RabbitMQClient()
            await cls._instance.start()
        return cls._instance

    async def start(self):
        self.connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue("task_queue", durable=True)

        # Start consuming tasks in the background
        asyncio.create_task(self.consume_tasks())

    async def consume_tasks(self):
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    # Handle the message asynchronously
                    await self.handle_message(message)

    async def publish_task(self, task_data):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=task_data.encode()),
            routing_key="task_queue",
        )
        print(f"Published task: {task_data}")

    async def handle_message(self, message):
        # Simulate an async call to a generative AI API
        data = message.body.decode()
        print(f"Received task: {data}")
        result = await self.call_ai_api(data)
        print(f"AI Response: {result}")

    async def call_ai_api(self, data):
        # Asynchronous HTTP call to a generative AI API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/endpoint", json={"input": data}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"API Error: {response.status}")
                    return {"error": f"API call failed with status {response.status}"}
