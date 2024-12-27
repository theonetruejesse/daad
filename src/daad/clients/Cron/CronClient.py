from typing import Any, Callable, Dict

from src.daad.clients.AppClient import AppClient
from src.daad.clients.Cron.Scheduler import CronScheduler, cron_job
from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient
from src.daad.constants import DAILY_LOG_CHANNEL, ISSUE_LOG_CHANNEL


class CronClient(AppClient):
    def __init__(self) -> None:
        self.scheduler: CronScheduler | None = None
        self.rabbitmq: RabbitMQClient | None = None

    async def _setup(self) -> None:
        """
        Acquire the shared RabbitMQClient, create our CronScheduler, define
        any static cron jobs, and start the scheduler.
        """
        self.rabbitmq = await RabbitMQClient.instance()
        self.scheduler = CronScheduler(self.rabbitmq)

        self._collect_decorated_jobs()
        self.scheduler.start()
        print("CronClient setup complete")

    async def cleanup(self) -> None:
        """
        Stop the scheduler and do any other necessary cleanup.
        """
        if self.scheduler:
            self.scheduler.stop()
            self.scheduler = None
        print("CronClient cleanup complete")

    def add_cron_job(
        self,
        func: Callable[..., Any],
        schedule: Dict[str, str],
        args: list[Any] | None = None,
    ) -> None:
        if not self.scheduler:
            raise RuntimeError("CronScheduler not initialized yet.")
        self.scheduler.add_cron_job(func, schedule, args)

    @cron_job(schedule={"hour": "8", "minute": "0"})  # Runs daily at 8:00
    async def send_morning_log(self) -> None:
        if not self.rabbitmq:
            raise RuntimeError("RabbitMQClient not available.")

        routing_key = "discord.notifications"
        message = f"{DAILY_LOG_CHANNEL}:Good morning!"
        print(f"[CronClient] -> send_morning_log -> {message}")
        await self.rabbitmq.publish(routing_key, message)

    @cron_job(schedule={"minute": "1"})  # Runs every minute
    async def canary_log(self) -> None:
        if not self.rabbitmq:
            raise RuntimeError("RabbitMQClient not available.")

        routing_key = "discord.notifications"
        message = f"{ISSUE_LOG_CHANNEL}:Canary log!"
        print(f"[CronClient] -> canary_log -> {message}")
        await self.rabbitmq.publish(routing_key, message)

    #
    # Internal method to discover and register any decorated methods from above
    #
    def _collect_decorated_jobs(self) -> None:
        """
        1) Find any methods in this class that have `_is_cron_job` set by the @cron_job decorator.
        2) Register them with `self.scheduler`.
        """
        if not self.scheduler:
            return

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and getattr(attr, "_is_cron_job", False):
                schedule = getattr(attr, "_schedule", {})
                # We'll pass an empty args=[] by default.
                # If you want to supply custom args, you can do that differently.
                self.scheduler.add_cron_job(attr, schedule, args=[])
