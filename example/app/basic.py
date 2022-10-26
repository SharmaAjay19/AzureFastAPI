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