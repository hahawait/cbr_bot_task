import betterlogging
from redis.asyncio import Redis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.exceptions import ResponseError


class RedisClient:
    _logger = betterlogging.getLogger("RedisClient")

    def __init__(self, connection: Redis):
        self.connection = connection
        self.idx = "idx:valute"

    async def create_idx(self) -> None:
        try:
            await self.connection.ft(self.idx).create_index(
                (
                    TextField("$.ID", as_name="ID"),
                    NumericField("$.NumCode", as_name="NumCode"),
                    TextField("$.CharCode", as_name="CharCode"),
                    NumericField("$.Nominal", as_name="Nominal"),
                    TextField("$.Name", as_name="Name"),
                    NumericField("$.Value", as_name="Value"),
                    NumericField("$.VunitRate", as_name="VunitRate"),
                ),
                definition=IndexDefinition(
                    prefix=["valute:"], index_type=IndexType.JSON
                ),
            )
            self._logger.info(f"Index {self.idx} created successfully")
        except ResponseError as e:
            self._logger.error(f"Error creating index: {e}")

    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        from_rate = await self.connection.ft(self.idx).search(
            Query(f"@CharCode:({from_currency})").return_field("Value")
        )
        to_rate = await self.connection.ft(self.idx).search(
            Query(f"@CharCode:({to_currency})").return_field("Value")
        )
        if from_rate.total == 0 or to_rate.total == 0:
            raise ValueError("Currency not found")
        from_value = float(from_rate.docs[0]["Value"])
        to_value = float(to_rate.docs[0]["Value"])
        return to_value / from_value

    async def get_all_rates(self) -> list[str]:
        total = (await self.connection.ft(self.idx).search("*")).total
        query = Query("*").paging(0, total)
        result = await self.connection.ft(self.idx).search(query)
        return [doc.__dict__["json"] for doc in result.docs]
