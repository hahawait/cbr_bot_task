import betterlogging
from redis.asyncio import Redis


class RedisClient:
    def __init__(self, connection: Redis):
        self.connection = connection

    async def create_or_update(self, data: list[tuple[str, str, dict]]) -> None:
        await self.connection.json().mset(data)
        betterlogging.info(f"Data updated successfully")
