import pytest
from client.api_client import APIClient
from lib.read_config import ConfigReader

@pytest.fixture(scope="session")
def api_client():
    config = ConfigReader()
    base_url = config.get_url()
    return APIClient(base_url)

@pytest.fixture(scope="session")
def auth_token(api_client):
    config = ConfigReader()
    payload = {
        "username": config.get_username(),
        "password": config.get_password()
    }
    response = api_client.post("/auth", json=payload)
    assert response.status_code == 200, "Auth token creation failed"

    token = response.json().get("token")
    assert token, "Token not found in auth response"

    return token

@pytest.fixture
def auth_headers(auth_token):
    return {
        "Cookie": "token={}".format(auth_token),
        "Content-Type": "application/json"
    }
