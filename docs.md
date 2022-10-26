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
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app.appConfig.hostname, port=app.appConfig.port)
```


### Connect to Redis cache and use in Middleware
```python
## HELPER FUNCTIONS
import time
def factorial(n, sleep=False):
    if sleep:
        time.sleep(4)
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

import os
## Import AzureFastAPI
from azurefastapi.azurefastapi import AzureFastAPI
from fastapi.responses import HTMLResponse
## Initialize with config
app = AzureFastAPI(os.path.join(os.path.dirname(__file__), "config.json"))

## Add middleware for caching (can do other operations as well)
@app.middleware("http")
async def http_request_middleware(request, call_next):
    return await app.useCaching(request, call_next)

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<center><h1>Welcome to AzureFastAPI</h1></center>"

@app.get("/hello")
async def root():
    return {"message": "Hello World"}

@app.get("/nfactorial/{n}")
async def nfactorial(n: int):
    return {"n": n, "n!": factorial(n, True)}

@app.get("/get/{userAlias}")
async def userInfo(userAlias: str):
    return {"message": app.redis.get(userAlias)}

# Run the azurefastapi app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app.appConfig.hostname, port=app.appConfig.port)
```

The config file looks like:
```json
{
    "hostname": "0.0.0.0",
    "port": "5002",
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
}
```