from typing import Any, Callable, Dict, List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.daad.clients.RabbitMQ.RabbitMQClient import RabbitMQClient


def cron_job(schedule: Dict[str, str]) -> Callable:
    """
    Decorator to mark methods as cron jobs and attach the schedule metadata.
    Use this in CronClient to mark methods as cron jobs.
    """

    def decorator(func: Callable) -> Callable:
        func._is_cron_job = True  # type: ignore
        func._schedule = schedule  # type: ignore
        return func

    return decorator


class CronScheduler:
    """
    A generic scheduling engine. It knows how to queue up jobs
    and run them with AsyncIOScheduler, but it doesn't own any
    "built-in" cron jobs by itself.
    """

    def __init__(self, rabbitmq: RabbitMQClient) -> None:
        self.scheduler = AsyncIOScheduler()
        self.rabbitmq: RabbitMQClient = rabbitmq
        self._cron_jobs: List[Dict[str, Any]] = []

    def add_cron_job(
        self,
        func: Callable[..., Any],
        schedule: Dict[str, str],
        args: List[Any] | None = None,
    ) -> None:
        """
        Allow other classes to add a new cron job at runtime without
        interrupting existing jobs.
        """
        if args is None:
            args = []

        job_def = {
            "func": func,
            "_schedule": schedule,
            "args": args,
        }
        self._cron_jobs.append(job_def)

        # If the scheduler is already running, schedule immediately.
        if self.scheduler.running:
            self._schedule_job(func, schedule, args)

    def start(self) -> None:
        """
        Schedule all known jobs and start the AsyncIOScheduler.
        """
        for job in self._cron_jobs:
            self._schedule_job(
                job["func"],
                job["_schedule"],
                job["args"],
            )

        self.scheduler.start()
        print("[CronScheduler] -> Started AsyncIOScheduler.")

    def stop(self) -> None:
        """
        Stop the scheduler gracefully.
        """
        self.scheduler.shutdown()
        print("[CronScheduler] -> Stopped AsyncIOScheduler.")

    #
    # Internal helper to schedule a single job.
    #
    def _schedule_job(
        self, func: Callable[..., Any], schedule: Dict[str, str], args: List[Any]
    ) -> None:
        """
        Schedules a single job using an AsyncIOScheduler CronTrigger.
        """
        self.scheduler.add_job(
            func,
            trigger=CronTrigger(**schedule),
            args=args,
        )
