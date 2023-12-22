from fastapi import FastAPI, HTTPException, Header, Request, APIRouter
from starlette.responses import JSONResponse
import requests
from typing import Annotated

auth = FastAPI()


@auth.middleware("http")
async def validate_token(request: Request, call_next, headers:Annotated[str | None, Header()] = None):
    print("reaching here---validateToken",headers)
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    auth_header_parts = auth_header.split(" ")

    if len(auth_header_parts) != 2 or auth_header_parts[0].lower() != "basic":
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    request.basicAuthToken = auth_header_parts[1]

    return await call_next(request)

@auth.middleware("http")
async def validate_session(request: Request, call_next):
    basic_auth_token = request.basicAuthToken
    session = request.json().get("session", {})
    token = session.get("token")
    required = session.get("required", False) if session else False
    method_body = request.json().get("methodBody", {})
    database = method_body.get("database")
    fm_server = request.json().get("fmServer")

    should_call_next = False  # Flag to track if next() should be called

    if not session or not token:
        try:
            fm_session_token = await fm_login(fm_server, database, basic_auth_token)

            if fm_session_token:
                is_session_valid = await fm_validate_session(fm_server, fm_session_token)

                if is_session_valid:
                    request.fmSessionToken = fm_session_token
                    should_call_next = True
                else:
                    return JSONResponse(status_code=401, content={"error": "Session token validation failed"})
        except Exception as error:
            return JSONResponse(status_code=401, content={"error": str(error)})
    else:
        try:
            is_session_valid = await fm_validate_session(fm_server, token)

            if is_session_valid:
                request.fmSessionToken = token
                should_call_next = True
            else:
                if token and (not required or required is False):
                    try:
                        fm_session_token = await fm_login(fm_server, database, basic_auth_token)

                        if fm_session_token:
                            is_session_valid = await fm_validate_session(fm_server, fm_session_token)

                            if is_session_valid:
                                request.fmSessionToken = fm_session_token
                                should_call_next = True
                            else:
                                return JSONResponse(status_code=401, content={"error": "Re-validation of session token failed"})
                        else:
                            return JSONResponse(status_code=401, content={"error": "Re-authentication failed"})
                    except Exception as error:
                        return JSONResponse(status_code=401, content={"error": str(error)})
                else:
                    return JSONResponse(status_code=401, content={"error": "Invalid session token"})
        except Exception as error:
            return JSONResponse(status_code=401, content={"error": "Session validation failed"})

    if should_call_next:
        await call_next(request)




async def fm_login(fm_server, database, basic_auth_token):
    print("reaching here---fmlogin")
    url = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/sessions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {basic_auth_token}"
    }
    
    try:
        login_response = requests.post(url, headers=headers, json={}, verify=False)
        print(login_response)
        login_response.raise_for_status()
        return login_response.json()["response"]["token"]
    except requests.HTTPError as error:
        print("fmLogin Error:", error)
        response_json = {
            "error": "An error occurred while logging in."
        }
        if error.response and error.response.status_code:
            response_json["statusText"] = error.response.status_code
            response_json["error"] = error.response.json()
        raise response_json

async def fm_validate_session(fm_server, session_token):
    print("reaching here---fmValidateSession")
    url = f"https://{fm_server}/fmi/data/vLatest/validateSession"
    
    headers = {
        "Authorization": f"Bearer {session_token}"
    }
    
    try:
        validate_response = requests.get(url, headers=headers, verify=False)
        validate_response.raise_for_status()
        return validate_response.json()["messages"][0]["message"] == "OK"
    except requests.HTTPError:
        return False  # Return false if there was an error


