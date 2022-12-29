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
from azurefastapi.azurefastapi import AzureFastAPI
from fastapi.responses import HTMLResponse
app = AzureFastAPI(os.path.join(os.path.dirname(__file__), "config.json"))

@app.middleware("http")
async def http_request_middleware(request, call_next):
    return await app.useCaching(request, call_next)

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<center><h1>Welcome to AzureFastAPI</h1></center>"

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/nfactorial/{n}")
async def nfactorial(n: int):
    return {"n": n, "n!": factorial(n, True)}

@app.get("/get/{userAlias}")
async def userInfo(userAlias: str):
    return {"message": app.redis.get(userAlias)}

@app.get("/getdb/{id}")
async def getDb(id: str):
    return await app.queryDb(
        "AllMeshes",
    f"SELECT * FROM mycontainer r WHERE r.name='{id}'")

# Run the azurefastapi app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app.appConfig.hostname, port=app.appConfig.port)