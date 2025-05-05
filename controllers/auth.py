from fastapi import FastAPI, HTTPException, Header, Request, APIRouter
from starlette.responses import JSONResponse
import requests

async def validate_token(req: Request):
    print("reaching here---validateToken")
    auth_header = req.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    auth_header_parts = auth_header.split(" ")

    if len(auth_header_parts) != 2 or auth_header_parts[0].lower() != "basic":
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    req.basicAuthToken = auth_header_parts[1]


async def validate_session(req: Request):
    basic_auth_token = req.basicAuthToken
    body= req.state.body
    session = body.get("session", {})
    token = session.get("token")
    required = session.get("required", False) if session else False
    method_body =body.get("methodBody", {})
    database = method_body.get("database")
    fm_server = body.get("fmServer")
    method=body.get("method")

    if not session or not token:
        try:
            fm_session_token = await fm_login(fm_server, database, basic_auth_token)

            if fm_session_token:
                is_session_valid = await fm_validate_session(fm_server, fm_session_token)
                if is_session_valid:
                    req.state.body["fmSessionToken"] = fm_session_token

                else:
                    return JSONResponse(status_code=401, content={"error": "Session token validation failed"})
        except Exception as error:
            return JSONResponse(status_code=401, content={"error": str(error)})
    else:
        try:
            is_session_valid = await fm_validate_session(fm_server, token)
            if is_session_valid:
                req.state.body["fmSessionToken"] = token
            else:
                if token:
                    try:
                        fm_session_token = await fm_login(fm_server, database, basic_auth_token)
                        if fm_session_token:
                            is_session_valid = await fm_validate_session(fm_server, fm_session_token)                            
                            if is_session_valid:
                                 req.state.body["fmSessionToken"] = fm_session_token

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

async def signin(req: Request):
  try:
        await validate_token(req)
        basic_auth_token = req.basicAuthToken
        body =req.state.body
        fm_server = body.get("fmServer")
        method_body = body.get("methodBody", {})
        database = method_body.get("database")

        if not fm_server or not database:
          raise HTTPException(status_code=400, detail="Missing fmServer or database in request body")

        session_token = await fm_login(fm_server, database, basic_auth_token)

        return {
          "message": "Signin Successful",
          "database": database,
          "session": session_token
        }
  except HTTPException as e:
        raise e
  except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signin failed: {str(e)}")

async def fm_login(fm_server, database, basic_auth_token):
    print("reaching here---fmlogin")
    url = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/sessions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {basic_auth_token}"
    }
    
    try:
        login_response = requests.post(url, headers=headers, json={}, verify=False)
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
    except requests.HTTPError as error:
        return False  # Return false if there was an error



async def signout(req: Request):
    try:
        body = req.state.body
        method_body = body.get("methodBody", {})
        database = method_body.get("database")
        fm_server = body.get("fmServer")
        token = body.get("fmSessionToken")

        if not (fm_server and database):
            raise HTTPException(status_code=400, detail="Missing fmServer, database.")
       
        url = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/sessions/{token}"
        headers = {
        "Authorization": f"Bearer {token}"
        }



        response = requests.delete(url, headers=headers, verify=False)
        if response.status_code == 200 and response.json().get("messages", [{}])[0].get("message") == "OK":
            return {"message": "Signout success"}
        else:
            return JSONResponse(status_code=401, content={"error": "Signout failed"})

    except requests.RequestException as error:
        response_json = {
            "error": "An error occurred while signing out.",
        }
        if error.response and error.response.status_code:
            response_json["statusText"] = error.response.status_code
            try:
                response_json["error"] = error.response.json()
            except Exception:
                response_json["error"] = str(error)
        return JSONResponse(status_code=500, content=response_json)