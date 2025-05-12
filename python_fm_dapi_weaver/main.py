from fastapi import FastAPI, APIRouter,HTTPException,UploadFile
from starlette.responses import Response
from .routes.index import router
import json


app = FastAPI()

app.include_router(router, prefix="/api")

# Routes
@app.get("/")
async def home():
    return "server is running"

# Middleware to parse request body
@app.middleware("http")
async def body_parser(request, call_next):
    content_type = request.headers.get("Content-Type", "")

    if "application/json" in content_type:

        # Parse the request body once and store it in request.state for easy access throughout the request 
        request.state.body = await request.json()
        
    elif "multipart/form-data" in content_type:
        form = await request.form()

        json_data = form.get("data")
        if not json_data:
            raise HTTPException(status_code=400, detail="Missing 'data' in form")
        try:
            request.state.body = json.loads(json_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in 'data'")
        file: UploadFile = form.get("file")
        
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        else:
            
            try:
                contents = await file.read()
                request.state.file = {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "data": contents
                }            
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")
            
    return await call_next(request)


def start_server(host="127.0.0.1", port=8000, reload=False):
    import uvicorn
    uvicorn.run("python_fm_dapi_weaver.main:app", host=host, port=port, reload=reload) 

if __name__ == "__main__":
    start_server(reload=True)  