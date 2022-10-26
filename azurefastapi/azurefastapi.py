from .models import AppConfig, CacheType, RedisCacheConfig
from fastapi import FastAPI
from .utils import loadResponse, processResponse
import os, redis, json

class AzureFastAPI(FastAPI):

    def __init__(self, configpath = None):
        super().__init__()
        try:
            if (configpath):
                config_content = json.loads(open(configpath, "r").read())
                self.appConfig = AppConfig.construct(**config_content)
                self.appConfig.cacheConfig=RedisCacheConfig.construct(**config_content["cacheConfig"])
            else:
                raise Exception("configpath not provided")
        except FileNotFoundError as e:
            self.appConfig = AppConfig()
        except Exception as e:
            print(str(e), "proceeding with default config")
            self.appConfig = AppConfig()  
        if self.appConfig.cacheEnabled and self.appConfig.cacheType == CacheType.redis:
            self.redis = redis.Redis(host=self.appConfig.cacheConfig.hostname, port=self.appConfig.cacheConfig.port, db=self.appConfig.cacheConfig.db, password=self.appConfig.cacheConfig.password, ssl=self.appConfig.cacheConfig.ssl)
    
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