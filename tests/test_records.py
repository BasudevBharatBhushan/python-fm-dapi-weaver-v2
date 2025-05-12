import json
import os
import base64
import requests
import pytest
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from .env

load_dotenv()

FM_SERVER = os.getenv("FM_SERVER")
FM_DATABASE = os.getenv("FM_DATABASE")
FM_LAYOUT = os.getenv("FM_LAYOUT")
FM_USERNAME = os.getenv("FM_USERNAME")
FM_PASSWORD = os.getenv("FM_PASSWORD")
URL = os.getenv("URL")

# signin should run only once,so session scope used
@pytest.fixture(scope="session")
def auth_headers():
    credentials = f"{FM_USERNAME}:{FM_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="session")
def fm_info():
    return {
        "server": FM_SERVER,
        "database": FM_DATABASE,
        "layout":  FM_LAYOUT
    }


@pytest.fixture(scope="session")
def signin_token(auth_headers, fm_info):

    payload = {
        "method": "signin",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"]
        },
         "session":{
            "token":"",
            "required":""
        }
    }



    response = requests.post(
        URL, 
        headers=auth_headers, 
        json=payload
    )
    assert response.status_code == 200
    assert "session" in response.json()
    assert response.json()["message"] == "Signin Successful"
    return response.json()["session"]


def test_get_all_records(auth_headers, fm_info, signin_token):

    payload = {
        "method": "getAllRecords",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"],
            "layout": fm_info["layout"]
        },
        "session": {
            "token": signin_token,
            "required": ""
        }
    }
    
    response = requests.post(URL, headers=auth_headers, json=payload)
    
    assert response.status_code == 200
    assert "records" in response.json()

def tes_find_record(auth_headers, fm_info, signin_token):
     
    payload = {
        "method": "findRecord",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"],
            "layout": fm_info["layout"],
            "query":[{"stock": 10}]
        },
        "session": {
            "token": signin_token,
            "required": ""
        }
    }
    response = requests.post(
        URL, 
        headers=auth_headers, 
        json=payload
    )
    assert response.status_code == 200
    assert "records" in response.json()

def tes_create_record(auth_headers, fm_info, signin_token):

    payload = {
        "method": "createRecord",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"],
            "layout": fm_info["layout"],
            "record": {
            "ProductName": "Vivo v50",
            "Description": " 5G 128 GB, 8 GB RAM, Mega Blue, Mobile Phone",
            "Category": "Electronics",
            "Price": 310000,
            "Stock": 20
          }
        },
        "session": {
            "token": signin_token,
            "required": ""
        }
    }
    response = requests.post(
        URL, 
        headers=auth_headers, 
        json=payload
    )
    assert response.status_code == 200
    assert response.json()["status"] == "created"

def tes_update_record(auth_headers, fm_info, signin_token):
    payload = {
        "method": "updateRecord",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"],
            "layout": fm_info["layout"],
            "recordId": "11", 
            "record":{
                "ProductName":"Vivo V50 5G",
                "Description":"Rose Red, 8GB RAM, 256GB Storage"
            }
        },
        "session": {
            "token": signin_token,
            "required": True
        }
    }
    response = requests.post(
        URL, 
        headers=auth_headers, 
        json=payload
    )
    assert response.status_code == 200

def tes_delete_record(auth_headers, fm_info, signin_token):
    payload = {
        "method": "deleteRecord",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"],
            "layout": fm_info["layout"],
            "recordId": "11"  
        },
        "session": {
            "token": signin_token,
            "required": True
        }
    }
    response = requests.post(
        URL, 
        headers=auth_headers, 
        json=payload
    )
    assert response.status_code == 200


def test_upload_container(auth_headers, fm_info, signin_token):
    file_path = Path.home() / "Downloads" / "vivo-v29.jpg"

    assert file_path.exists(), f"File not found at {file_path}"

    with open(file_path, "rb") as f:
        file_data = f.read()

    json_payload = {
        "method": "uploadContainer",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"],
            "layout": fm_info["layout"],
            "recordId": "9", 
            "fieldName": "Image",  
            "repetition": 1
        },
        "session": {
            "token": signin_token,
            "required": ""
        }
    }

    files = {
        "data": (None, json.dumps(json_payload), "application/json"),
        "file": ("vivo-v29.jpg", file_data, "image/jpeg")
    }



    response = requests.post(
        URL,
        headers={k: v for k, v in auth_headers.items() if k.lower() != "content-type"},
        files=files
    )


    assert response.status_code == 200
    assert response.json()["status"] == "uploaded"
 
 
def test_signout(auth_headers, fm_info,signin_token):

    signout_payload = {
        "method": "signout",
        "fmServer": fm_info["server"],
        "methodBody": {
            "database": fm_info["database"]
        },
        "session": {
            "token": signin_token,
            "required": ""
        }
    }



    response = requests.post(
        URL,
        headers=auth_headers,
        json=signout_payload
    )


    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Signout success"
