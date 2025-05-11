import json
import pytest
import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

FM_SERVER = os.getenv("FM_SERVER")
FM_DATABASE = os.getenv("FM_DATABASE")
FM_USERNAME = os.getenv("FM_USERNAME")
FM_PASSWORD = os.getenv("FM_PASSWORD")
URL = os.getenv("URL")


@pytest.fixture
def auth_headers():
    credentials = f"{FM_USERNAME}:{FM_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def fm_info():
    return {
        "server": FM_SERVER,
        "database": FM_DATABASE,
    }


@pytest.fixture
def signin_token(auth_headers, fm_info):

    json_payload = {
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
        json=json_payload
    )


    assert response.status_code == 200, response.text
    assert "session" in response.json()
    assert response.json()["message"] == "Signin Successful"
    return response.json()["session"]



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
 