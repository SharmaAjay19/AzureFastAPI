from .models import AppConfig, CacheType, CosmosDbConfig, DatabaseType, RedisCacheConfig, StaticContentConfig
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .utils import loadResponse, processResponse
import redis, json
from azure.cosmos import CosmosClient

class AzureFastAPI(FastAPI):

    def __init__(self, configpath = None):
        super().__init__(title = "AzureFastAPI")
        try:
            if (configpath):
                config_content = json.loads(open(configpath, "r").read())
                self.appConfig = AppConfig.construct(**config_content)
                self.appConfig.cacheConfig=RedisCacheConfig.construct(**config_content["cacheConfig"])
                self.appConfig.staticContentConfig = StaticContentConfig.construct(**config_content["staticContentConfig"])
                self.appConfig.cosmosConfig = CosmosDbConfig.construct(**config_content["cosmosConfig"])
            else:
                raise Exception("configpath not provided")
        except FileNotFoundError as e:
            self.appConfig = AppConfig()
        except Exception as e:
            print(str(e), "proceeding with default config")
            self.appConfig = AppConfig()
        if self.appConfig.staticContentConfig and self.appConfig.staticContentConfig.staticFolder:
            self.mount("/static", StaticFiles(directory=self.appConfig.staticContentConfig.staticFolder), name="static")
        if self.appConfig.cacheEnabled and self.appConfig.cacheType == CacheType.redis:
            self.redis = redis.Redis(host=self.appConfig.cacheConfig.hostname, port=self.appConfig.cacheConfig.port, db=self.appConfig.cacheConfig.db, password=self.appConfig.cacheConfig.password, ssl=self.appConfig.cacheConfig.ssl)
        if self.appConfig.dbEnabled and self.appConfig.dbType == DatabaseType.cosmos:
            self.cosmos = CosmosClient(self.appConfig.cosmosConfig.cosmosAccountUri, credential = self.appConfig.cosmosConfig.cosmosAccountKey)
            if self.appConfig.cosmosConfig.cosmosDatabase:
                self.cosmos.db = self.cosmos.get_database_client(self.appConfig.cosmosConfig.cosmosDatabase)
    
    async def queryDb(self, containername, query):
        container = self.cosmos.db.get_container_client(containername)
        results = []
        for item in container.query_items(
            query=query,
            enable_cross_partition_query=True):
            results.append(item)
        return results

    async def useCaching(self, request, call_next):
        if self.appConfig.cacheEnabled and [x for x in self.appConfig.cacheEnabledPaths if request.url.path.startswith(x)]:
            response = self.getFromCache(request.url.path)
            if not response:
                response = await call_next(request)
                response = await self.saveToCache(request.url.path, response)
            return response
        else:
            return await call_next(request)
    
    def enableRequestCaching(self):
        self.requestCachingEnabled = True
    
    async def saveToCache(self, url_path, response):
        json_response, response = await processResponse(response)
        self.redis.set(url_path, json.dumps(json_response))
        return response

    def getFromCache(self, url_path):
        from_cache = self.redis.get(url_path)
        if from_cache:
            response = loadResponse(json.loads(from_cache))
            response.headers["x-from-cache"] = "true"
            return response
        return None