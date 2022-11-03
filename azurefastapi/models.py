from optparse import Option
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class DatabaseType(str, Enum):
    cosmos = "cosmos"

class CacheType(str, Enum):
    redis = "redis"
    memcached = "memcached"

class RedisCacheConfig(BaseModel):
    hostname: str
    port: int
    password: str
    db: int
    ssl: bool

class CosmosDbConfig(BaseModel):
    cosmosAccountUri: Optional[str] = None
    cosmosAccountKey: Optional[str] = None
    cosmosDatabase: Optional[str] = None

class StaticContentConfig(BaseModel):
    staticFolder: str
    preLoad: Optional[bool] = False

class AppConfig(BaseModel):
    hostname: str = "0.0.0.0"
    port: int = 3002
    cacheEnabled: Optional[bool] = False
    cacheEnabledPaths: List[str] = []
    cacheType: Optional[CacheType] = CacheType.redis
    cacheConfig: Optional[RedisCacheConfig] = None
    dbEnabled: Optional[bool] = False
    dbType: Optional[DatabaseType] = DatabaseType.cosmos
    cosmosConfig: Optional[CosmosDbConfig] = None
    staticContentConfig: Optional[StaticContentConfig] = None