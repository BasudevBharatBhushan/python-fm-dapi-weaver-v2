import requests
import json
from fastapi import APIRouter, HTTPException


async def create_record(req: dict):
    token = req["fmSessionToken"]
    record = req["body"]["methodBody"]["record"]
    database = req["body"]["methodBody"]["database"]
    layout = req["body"]["methodBody"]["layout"]
    fm_server = req["body"]["fmServer"]

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
            "session": req["fmSessionToken"]
        }
    except requests.HTTPError as e:
        error_message = "An error occurred while creating the record."
        if e.response:
            error_message = e.response.json()
        raise HTTPException(status_code=500, detail=error_message)


async def get_all_records(req: dict):
    token = req["fmSessionToken"]
    database = req["body"]["methodBody"]["database"]
    layout = req["body"]["methodBody"]["layout"]
    fm_server = req["body"]["fmServer"]
    offset = req["body"]["methodBody"]["offset"]
    limit = req["body"]["methodBody"]["limit"]

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

        if "messages" in response.json().get("data", {}) and response.json()["messages"][0]["message"] == "OK":
            records = [record["fieldData"] for record in response.json()["response"]["data"]]
            record_info = response.json()["response"]["dataInfo"]

            return {
                "recordInfo": {
                    "table": record_info["table"],
                    "layout": record_info["layout"],
                    "totalRecordCount": record_info["totalRecordCount"]
                },
                "records": records,
                "session": req["fmSessionToken"]
            }
    except requests.HTTPError as e:
        error_message = "An error occurred while fetching the record."
        if e.response:
            error_message = e.response.json()
        raise HTTPException(status_code=500, detail=error_message)


async def update_record(req: dict):
    token = req["fmSessionToken"]
    record = req["body"]["methodBody"]["record"]
    database = req["body"]["methodBody"]["database"]
    layout = req["body"]["methodBody"]["layout"]
    record_id = req["body"]["methodBody"]["recordId"]
    fm_server = req["body"]["fmServer"]

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
            "session": req["fmSessionToken"]
        }
    except requests.HTTPError as e:
        error_message = "An error occurred while updating the record."
        if e.response:
            error_message = e.response.json()
        raise HTTPException(status_code=500, detail=error_message)


async def find_record(req: dict):
    token = req["fmSessionToken"]
    method_body = req["body"]["methodBody"]
    database = method_body["database"]
    layout = method_body["layout"]

    request_body = {
        "query": method_body["query"],
        "sort": method_body["sort"],
        "limit": method_body["limit"],
        "offset": method_body["offset"],
        "portal": method_body["portal"],
        "dateformats": method_body["dateformats"],
        "layout.response": method_body["layout.response"]
    }

    if method_body.get("scripts"):
        scripts = method_body["scripts"]
        request_body.update({
            "script": scripts.get("script"),
            "script.param": scripts.get("script.param"),
            "script.prerequest": scripts.get("script.prerequest"),
            "script.prerequest.param": scripts.get("script.prerequest.param"),
            "script.presort": scripts.get("script.presort"),
            "script.presort.param": scripts.get("script.presort.param")
        })

    apiUrl = f"https://{req['body']['fmServer']}/fmi/data/vLatest/databases/{database}/layouts/{layout}/_find"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(apiUrl, json=request_body, headers=headers, verify=False)
        response.raise_for_status()

        if "messages" in response.json().get("data", {}) and response.json()["messages"][0]["message"] == "OK":
            records = [record["fieldData"] for record in response.json()["response"]["data"]]
            record_info = response.json()["response"]["dataInfo"]

            return {
                "recordInfo": {
                    "table": record_info["table"],
                    "layout": record_info["layout"],
                    "totalRecordCount": record_info["foundCount"]
                },
                "records": records,
                "session": req["fmSessionToken"]
            }
    except requests.HTTPError as e:
        error_message = "An error occurred while fetching the record."
        if e.response:
            error_message = e.response.json()
        raise HTTPException(status_code=500, detail=error_message)
