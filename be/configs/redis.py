import redis

REDIS_URL = "redis://localhost:6379"


def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(REDIS_URL)
