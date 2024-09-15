import aioredis
from typing import Optional
import json

# Configure Redis connection
REDIS_URL = "redis://localhost:6379"
redis = aioredis.from_url(REDIS_URL)

async def set_cache(key: str, value: dict, expire: int = 3600):
    """Set a value in Redis cache with an expiration time."""
    await redis.set(key, json.dumps(value), ex=expire)

async def get_cache(key: str) -> Optional[dict]:
    """Retrieve a value from Redis cache."""
    cached_value = await redis.get(key)
    if cached_value:
        return json.loads(cached_value)
    return None
