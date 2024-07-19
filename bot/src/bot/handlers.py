import betterlogging
from aiogram import Router, types
from aiogram.filters import Command

from db.client import RedisClient
from db.schemas import Valute

bot_router = Router(name="bot_router")


@bot_router.message(Command("exchange"))
async def exchange_rate(message: types.Message, redis_client: RedisClient):
    try:
        _, from_currency, to_currency, amount = message.text.split()
        amount = float(amount)
        rate = await redis_client.get_exchange_rate(from_currency, to_currency)
        result = rate * amount
        await message.reply(f"{amount} {from_currency} = {result:.2f} {to_currency}")
    except ValueError as e:
        await message.reply(f"Ошибка: {e}")
    except Exception as e:
        betterlogging.error(f"Error handling /exchange command: {e}")
        await message.reply("Произошла ошибка при обработке команды.")


@bot_router.message(Command("rates"))
async def all_rates(message: types.Message, redis_client: RedisClient):
    rates = [Valute.model_validate_json(rate) for rate in (await redis_client.get_all_rates())]
    response = "\n".join(
        [
            f"<b>{rate.Name} ({rate.CharCode}):</b> {rate.Value}" for rate in rates
        ]
    )
    await message.reply(response, parse_mode="HTML")
