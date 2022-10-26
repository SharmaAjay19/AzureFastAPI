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
## Initialize with config
app = AzureFastAPI(os.path.join(os.path.dirname(__file__), "config.json"))

## Add middleware for caching (can do other operations as well)
@app.middleware("http")
async def http_request_middleware(request, call_next):
    response = app.getFromCache(request.url.path)
    if not response:
        response = await call_next(request)
        response = await app.saveToCache(request.url.path, response)
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to AzureFastAPI!"}

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