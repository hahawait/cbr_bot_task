from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from bot.handlers import bot_router
from db.client import RedisClient

from config import Config


async def run_bot(config: Config, redis_client: RedisClient) -> None:
    bot = Bot(
        token=config.bot_config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(
        redis_client=redis_client
    )
    dp.include_router(bot_router)
    await dp.start_polling(bot)
