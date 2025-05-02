from fastapi import HTTPException
import requests

def handle_api_error(e: requests.HTTPError, message: str = "An error occurred"):
    if e.response is not None:
        try:
            return HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json()
            )
        except Exception:
            return HTTPException(
                status_code=e.response.status_code,
                detail=e.response.text or message
            )
    return HTTPException(status_code=500, detail=message)
 