import requests
import json
import base64
from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from ..utils.helpers import handle_api_error,validate_required_params

async def create_record(req: Request):
    data = req.state.body
    token =   req.state.fmSessionToken
    method_body = data.get("methodBody", {})
    record = method_body.get("record")
    database = method_body.get("database")
    layout = method_body.get("layout") 
    fm_server = data.get("fmServer") 

    validate_required_params({
        "fmSessionToken": token,
        "fmServer": fm_server,
        "database": database,
        "layout": layout,
        "record": record

    })

    apiUrl = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/layouts/{layout}/records"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    requestData = {
        "fieldData": record
    }

    try:
        response = requests.post(apiUrl, headers=headers, json=requestData, verify=False)
        response.raise_for_status()
        recordId = response.json().get("response", {}).get("recordId")
        return {
            "status": "created",
            "recordId": recordId,
            "fieldData": record,
            "session": token
        }
        
    except requests.HTTPError as e:
        raise handle_api_error(e,"An error occurred while creating the record.")


async def get_all_records(req: Request):
    data = req.state.body
    token =  req.state.fmSessionToken
    method_body = data.get("methodBody", {})
    database = method_body.get("database")
    layout = method_body.get("layout")  
    fm_server = data.get("fmServer") 
    offset = method_body.get("offset")
    limit =  method_body.get("limit")

    validate_required_params({
        "fmSessionToken": token,
        "fmServer": fm_server,
        "database": database,
        "layout": layout
    })

    
    apiUrl = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/layouts/{layout}/records"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    query_params = {
        "_offset": offset,
        "_limit": limit
    }

    try:
        response = requests.get(apiUrl, params=query_params, headers=headers, verify=False)
        response.raise_for_status()
        json_data = response.json()
        if "messages" in json_data and json_data["messages"][0]["message"] == "OK":
            # records = [record["fieldData"] for record in response.json()["response"]["data"]]
            records = [{
                 "recordId": record["recordId"],
                 **record["fieldData"]
                 } for record in json_data["response"]["data"]]

            record_info = json_data["response"]["dataInfo"]

            return {
                "recordInfo": {
                    "table": record_info["table"],
                    "layout": record_info["layout"],
                    "totalRecordCount": record_info["totalRecordCount"],
                    "foundCount": record_info["foundCount"],
                },
                "records": records,
                "session": token
            }
    except requests.HTTPError as e:
        raise handle_api_error(e,"An error occurred while fetching the records.")


async def update_record(req:Request):

    data = req.state.body
    token =   req.state.fmSessionToken
    fm_server = data.get("fmServer") 
    method_body = data.get("methodBody", {})
    record = method_body.get("record")
    database = method_body.get("database")
    layout = method_body.get("layout") 
    record_id = method_body.get("recordId")
    validate_required_params({
        "fmSessionToken": token,
        "fmServer": fm_server,
        "database": database,
        "layout": layout,
        "recordId": record_id,
    })

   

    apiUrl = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/layouts/{layout}/records/{record_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    requestData = {
        "fieldData": record
    }

    try:
        response = requests.patch(apiUrl, json=requestData, headers=headers, verify=False)
        response.raise_for_status()

        return {
            "status": "updated",
            "recordId": record_id,
            "fieldData": record,
            "session": token
        }
    except requests.HTTPError as e:
        raise handle_api_error(e,"An error occurred while updating the record.")


async def find_record(req: Request):

    data = req.state.body
    token =   req.state.fmSessionToken
    method_body = data.get("methodBody", {})
    database = method_body.get("database")
    layout = method_body.get("layout") 
    fm_server = data.get("fmServer") 

    validate_required_params({
        "fmSessionToken": token,
        "fmServer": fm_server,
        "database": database,
        "layout": layout
    })

   
    request_body = {
        "query": method_body.get("query"),
        "sort": method_body.get("sort"),
        "limit": method_body.get("limit"),
        "offset": method_body.get("offset"),
        "portal": method_body.get("portal"),
        "dateformats": method_body.get("dateformats"),
        "layout.response": method_body.get("layout.response")
    }

    if method_body.get("scripts"):
        scripts = method_body.get("scripts")
        request_body.update({
            "script": scripts.get("script"),
            "script.param": scripts.get("script.param"),
            "script.prerequest": scripts.get("script.prerequest"),
            "script.prerequest.param": scripts.get("script.prerequest.param"),
            "script.presort": scripts.get("script.presort"),
            "script.presort.param": scripts.get("script.presort.param")
        })
    request_body = {key: val for key, val in request_body.items() if val is not None}

    apiUrl = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/layouts/{layout}/_find"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(apiUrl, json=request_body, headers=headers, verify=False)
        response.raise_for_status()
        json_data = response.json()
        if "messages" in json_data  and json_data["messages"][0]["message"] == "OK":
            records = [{
                 "recordId": record["recordId"],
                 **record["fieldData"]
                 } for record in json_data["response"]["data"]]
            record_info = json_data["response"]["dataInfo"]

            return {
                "recordInfo": {
                    "table": record_info["table"],
                    "layout": record_info["layout"],
                    "totalRecordCount": record_info["totalRecordCount"],
                    "foundCount": record_info["foundCount"],
                },
                "records": records,
                "session": token
            }
    except requests.HTTPError as e:
        raise handle_api_error(e,"An error occurred while fetching the record.")

async def delete_record(req: Request):
    data = req.state.body
    token =   req.state.fmSessionToken
    method_body = data.get("methodBody", {})
    database = method_body.get("database")
    layout = method_body.get("layout")
    record_id = method_body.get("recordId")
    fm_server = data.get("fmServer")

    validate_required_params({
        "fmSessionToken": token,
        "fmServer": fm_server,
        "database": database,
        "layout": layout,
        "recordId": record_id,
    })

    
    if not all([database, layout, record_id, fm_server]):
        raise HTTPException(status_code=400, detail="Missing required parameters")

    apiUrl = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/layouts/{layout}/records/{record_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(apiUrl, headers=headers, verify=False)
        response.raise_for_status()

        return {
            "status": "deleted",
            "recordId": record_id,
            "session": token
        }

    except requests.HTTPError as e:
        raise handle_api_error(e,"An error occurred while deleting the record.")
 
async def upload_container(req: Request):
    try:
        file_info = getattr(req.state, "file", None)
        if not file_info:
            raise HTTPException(status_code=400, detail="No file uploaded")
        file_content = file_info["data"]
        file_name = file_info["filename"]
        file_type = file_info["content_type"]

        files = {
            'upload': (file_name, file_content, file_type)
        }
        data = req.state.body
        token =   req.state.fmSessionToken 
        fm_server = data.get("fmServer")
        method_body = data.get("methodBody", {})
        database = method_body.get("database")
        layout = method_body.get("layout")
        record_id = method_body.get("recordId")
        field_name = method_body.get("fieldName")

        validate_required_params({
            "fmSessionToken": token,
            "fmServer": fm_server,
            "database": database,
            "layout": layout,
            "recordId": record_id,
            "fieldName": field_name,
        })

        api_url = f"https://{fm_server}/fmi/data/vLatest/databases/{database}/layouts/{layout}/records/{record_id}/containers/{field_name}"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.post(
                    api_url,
                    files=files,
                    headers=headers,
                    verify=False 
            )
            response.raise_for_status()

            return {
                    "status": "uploaded",
                    "recordId": record_id,
                    "fieldName": field_name,
                    "fileName": file_name,
                    "session": token
            }

        except requests.HTTPError as e:
            raise handle_api_error(e,"An error occurred while uploading the file.")

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

