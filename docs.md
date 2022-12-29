## Usage

### Basic
```python
from azurefastapi.azurefastapi import AzureFastAPI
from fastapi.responses import HTMLResponse
app = AzureFastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<center><h1>Welcome to AzureFastAPI</h1></center>"

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app.appConfig.hostname, port=app.appConfig.port)
```


### Connect to Redis cache and use in Middleware
```python
## Initialize with config
app = AzureFastAPI(os.path.join(os.path.dirname(__file__), "config.json"))

## Add middleware for caching (can do other operations as well)
@app.middleware("http")
async def http_request_middleware(request, call_next):
    return await app.useCaching(request, call_next)

@app.get("/nfactorial/{n}")
async def nfactorial(n: int):
    return {"n": n, "n!": factorial(n, True)}

@app.get("/get/{userAlias}")
async def userInfo(userAlias: str):
    return {"message": app.redis.get(userAlias)}

```

The config file looks like:
```json
{
    ...
    "cacheEnabled": true,
    "cacheEnabledPaths": ["/nfactorial"],
    "cacheType": "redis",
    "cacheConfig": {
        "hostname": "localhost",
        "port": 3002,
        "password": null,
        "db": 0,
        "ssl": false
    }
    ...
}
```