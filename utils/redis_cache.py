import json
from typing import Any, Optional
import redis.asyncio as redis
from config import Config
from utils.logger import logger


class RedisCache:
    def __init__(self):
        self.redis = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            decode_responses=True
        )

    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """
        Set a key with value in Redis with optional
        expiration (default 1 hour)
        """
        try:
            await self.redis.set(key, json.dumps(value), ex=expire)
        except Exception as e:
            logger.error(f"Error setting Redis key {key}: {str(e)}")

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis by key"""
        try:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting Redis key {key}: {str(e)}")
            return None

    async def delete(self, key: str) -> None:
        """Delete a key from Redis"""
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Error deleting Redis key {key}: {str(e)}")

    async def close(self) -> None:
        """Close Redis connection"""
        await self.redis.close()
