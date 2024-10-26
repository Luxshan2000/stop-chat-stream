import aioredis
from fastapi import FastAPI


async def connect_to_redis():
    # Redis connection logic here
    redis = await aioredis.from_url("redis://localhost")
    return redis


async def close_redis_connection(redis):
    await redis.close()
