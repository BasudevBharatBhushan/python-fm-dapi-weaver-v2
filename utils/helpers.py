from fastapi import HTTPException
import requests

def validate_required_params(params: dict):
    # Validate required parameters and raise error if any param missing.
    missing = [k for k, v in params.items() if not v]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required parameters: {', '.join(missing)}")

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