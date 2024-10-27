from redis import Redis

from be.db.models import AbortSignal


def save_abort_signal_to_redis(id: str, flag: bool, redis_client: Redis):
    key = f"abort:{id}"
    redis_client.hset(key, mapping={"id": id, "flag": int(flag)})
    redis_client.close()


def get_abort_signal_from_redis(id: str, redis_client: Redis) -> AbortSignal:
    key = f"abort:{id}"
    data = redis_client.hgetall(key)
    redis_client.close()

    if data:
        return AbortSignal(id=data[b"id"].decode(), flag=bool(int(data[b"flag"])))

    return None


def update_abort_signal_in_redis(id: str, flag: bool, redis_client: Redis):
    key = f"abort:{id}"
    if redis_client.exists(key):
        redis_client.hset(key, "flag", int(flag))
        redis_client.close()

        return True
    redis_client.close()

    return False


def delete_abort_signal_from_redis(id: str, redis_client: Redis) -> bool:
    key = f"abort:{id}"
    if redis_client.exists(key):
        redis_client.delete(key)
        redis_client.close()
        return True
    redis_client.close()
    return False
