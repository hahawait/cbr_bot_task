import asyncio
import betterlogging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apps.bank.dependencies import get_bank_service
from apps.base.redis_client import RedisClient

from apps.db import RedisConnection
from config import get_config

config = get_config()
betterlogging.basic_colorized_config(level="INFO")


async def main():
    bank_service = get_bank_service(config)
    valutes = await bank_service.get_exchange_rates()

    async with RedisConnection(config.redis_config.redis_url) as connection:
        client = RedisClient(connection.get_client())
        await client.create_or_update(data=valutes)


def schedule_task():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(main, 'interval', days=1)
    scheduler.add_job(main, 'interval', days=1, next_run_time=datetime.now())

    scheduler.start()


if __name__ == "__main__":
    schedule_task()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        betterlogging.info("Shutting down...")
