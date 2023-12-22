from fastapi import APIRouter, Request, Response
from controllers.index import data_api

router = APIRouter()

@router.post("/dataApi")
async def data_api_route(req: dict, res: Response):
    return await data_api(req, res)
