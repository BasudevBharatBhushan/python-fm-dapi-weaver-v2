from fastapi import FastAPI, APIRouter
from starlette.responses import Response
from routes.index import router

app = FastAPI()

app.include_router(router, prefix="/api")

# Routes
@app.get("/")
async def home():
    return "Python-dapi-server is running"


# Middleware equivalent - Similar to app.use() in Express
@app.middleware("http")
async def custom_middleware(request, call_next):
    if request.headers.get("Content-Type") == "application/json":
        try:
            request.state.body = await request.json()
        except Exception as e:
           raise HTTPException(status_code=400, detail="Invalid JSON")
    return await call_next(request)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)