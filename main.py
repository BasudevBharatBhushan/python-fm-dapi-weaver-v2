from fastapi import FastAPI, APIRouter
from starlette.responses import Response
from routes.index import router

app = FastAPI()
app.include_router(router)

# Routes
@app.get("/")
async def home():
    return "Python-dapi-server is running"

app.include_router(router, prefix="/api")

# Middleware equivalent - Similar to app.use() in Express
@app.middleware("http")
async def custom_middleware(request, call_next):
    # Add middleware logic here if needed
    response = await call_next(request)
    return response

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
