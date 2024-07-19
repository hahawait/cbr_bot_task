import betterlogging

import redis.asyncio as redis


class RedisConnection:
    _instance = None
    _pool = None
    _logger = betterlogging.getLogger("RedisConnection")

    def __new__(
            cls,
            url: str = None,
            host: str = "localhost",
            port: int = 6379,
            password: str = None,
            db: int = 0,
    ) -> "RedisConnection":
        if cls._instance is None:
            cls._instance = super(RedisConnection, cls).__new__(cls)
            if url:
                cls._pool = redis.ConnectionPool.from_url(url)
                cls._logger.info("Redis connection pool initialized from URL")
            else:
                cls._pool = redis.ConnectionPool(
                    host=host,
                    port=port,
                    password=password,
                    db=db,
                )
                cls._logger.info("Redis connection pool initialized")
        return cls._instance

    @classmethod
    def get_client(cls):
        if cls._pool is None:
            raise ConnectionError("Redis connection pool is not initialized")
        return redis.Redis(connection_pool=cls._pool)

    @classmethod
    async def close(cls):
        if cls._pool is not None:
            await cls._pool.disconnect()
            cls._logger.info("Redis Connection Pool have been closed successfully!!!")
        else:
            cls._logger.info("Connection already closed!!!")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
