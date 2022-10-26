from typing import Optional
from pydantic import BaseModel
from enum import Enum

class CacheType(str, Enum):
    redis = "redis"
    memcached = "memcached"

class RedisCacheConfig(BaseModel):
    hostname: str
    port: int
    password: str
    db: int
    ssl: bool

class AppConfig(BaseModel):
    hostname: str = "0.0.0.0"
    port: int = 3002
    cacheEnabled: Optional[bool] = False
    cacheType: Optional[CacheType] = CacheType.redis
    cacheConfig: Optional[RedisCacheConfig] = None
    staticFolder: Optional[str] = None