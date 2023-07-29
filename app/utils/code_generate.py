from __future__ import annotations

from datetime import timedelta
from redis.asyncio import Redis

from app.models.user import User
import random


def generate_code() -> int:
    return random.randrange(100000, 999999)


async def add_code_to_redis(
        redis_client: Redis,
        email: str,
        code: int,
        expire_time: int | None = 1,
):
    code_key = f"code:{email}:{code}"
    valid_token = await get_valid_code(redis_client, email, code)
    await redis_client.sadd(code_key, code)
    if not valid_token:
        await redis_client.expire(code_key, timedelta(minutes=expire_time))


async def get_valid_code(redis_client: Redis, email: str, code: int):
    code_key = f"code:{email}:{code}"
    valid_code = await redis_client.smembers(code_key)
    return valid_code
