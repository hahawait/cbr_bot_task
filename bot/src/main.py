import asyncio
import betterlogging

from bot.client import run_bot
from db.client import RedisClient
from db.connection import RedisConnection

from config import get_config

config = get_config()

betterlogging.basic_colorized_config(level=betterlogging.INFO)


async def main():
    conn = RedisConnection(config.redis_config.redis_url)
    redis = RedisClient(
        conn.get_client()
    )
    await redis.create_idx()

    await run_bot(config, redis)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        betterlogging.info("Shutting down...")
