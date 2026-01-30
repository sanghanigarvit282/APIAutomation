import os
from datetime import datetime

import pytest

import global_variables
from client.api_client import APIClient
from lib.read_config import ConfigReader

@pytest.fixture(scope="session")
def api_client(config_env):
    base_url = config_env.get_url()
    return APIClient(base_url)

@pytest.fixture(scope="session")
def auth_token(config_env,api_client):
    payload = {
        "username": config_env.get_username(),
        "password": config_env.get_password()
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

def pytest_metadata(metadata):
    metadata.clear()
    metadata.update({
        "Project Name": "API Automation",
        "Tester": "Garvit Sanghani",
        "Environment": "QA",
        "OS": "Windows",
        "Python Version": "3.9",
        "Framework": "PyTest + Requests",
    })

@pytest.hookimpl()
def pytest_html_report_title(report):
    report.title = "API Automation Test Report"

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against (dev / prod)"
    )

def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

    base_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(base_dir, exist_ok=True)

    run_dir = os.path.join(base_dir, f"test_{timestamp}")
    global_variables.report_path = os.path.join(run_dir, "report.html")

    global_variables.current_run_dir = run_dir

    config.option.htmlpath = global_variables.report_path

@pytest.fixture(scope="session")
def config_env(request):
    env = request.config.getoption("--env")
    return ConfigReader(env)