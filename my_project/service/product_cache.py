
"""Redis cache for products."""

import os

from flask import current_app
from redis import Redis, RedisError


CACHE_ENABLED = os.getenv("CACHE_ENABLED", "false").lower() == "true"
CACHE_TTL = 30

redis_client = (
    Redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1
    )
    if CACHE_ENABLED else None
)


def get_or_load(product_id, load_from_db):
    if not CACHE_ENABLED:
        return load_from_db(), "OFF"

    key = f"product:{product_id}"

    try:
        cached = redis_client.get(key)
        if cached is not None:
            return current_app.json.loads(cached), "HIT"
    except (RedisError, ValueError):
        current_app.logger.warning("Redis cache read failed")
        return load_from_db(), "ERROR"

    product = load_from_db()

    if product is not None:
        try:
            redis_client.setex(
                key,
                CACHE_TTL,
                current_app.json.dumps(product)
            )
        except RedisError:
            current_app.logger.warning("Redis cache write failed")
            return product, "ERROR"

    return product, "MISS"


def invalidate(product_id):
    if not CACHE_ENABLED:
        return

    try:
        redis_client.delete(f"product:{product_id}")
    except RedisError:
        current_app.logger.warning("Redis cache invalidation failed")
