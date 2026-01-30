import os
from datetime import datetime

import pytest

import global_variables
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
    """
    Based on the argument, set the config parameters
    :param parser: {object} parser object
    :return: None
    """
    parser.addoption(
        "--baseurl",
        action="store",
        default= None,
        help="Base URL for API execution",
        type=str
    )

@pytest.fixture(scope="session", autouse=True)
def apply_cli_overrides(request):
    """
    Applies command-line configuration overrides to the framework settings.

    This function reads values passed via pytest command-line arguments
    (such as browser, environment, or base URL) and overrides the
    corresponding configuration values loaded from the config file.
    """
    config = ConfigReader()
    base_url = request.config.getoption("--baseurl")

    if base_url:
        config.set_override("url", base_url)

def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

    base_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(base_dir, exist_ok=True)

    run_dir = os.path.join(base_dir, f"test_{timestamp}")
    global_variables.report_path = os.path.join(run_dir, "report.html")

    global_variables.current_run_dir = run_dir

    config.option.htmlpath = global_variables.report_path
