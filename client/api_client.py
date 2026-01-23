import requests

class APIClient:
    """
    A simple HTTP API client wrapper around the requests library.
    This client provides methods for common HTTP methods
    (GET, POST, PUT, DELETE) with a configurable base URL and timeout.
    """
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, endpoint, headers=None):
        return requests.get(
            "{}{}".format(self.base_url, endpoint),
            headers=headers,
            timeout=self.timeout
        )

    def post(self, endpoint, json=None, headers=None):
        return requests.post(
            "{}{}".format(self.base_url, endpoint),
            json=json,
            headers=headers,
            timeout=self.timeout
        )

    def put(self, endpoint, json=None, headers=None):
        return requests.put(
            "{}{}".format(self.base_url, endpoint),
            json=json,
            headers=headers,
            timeout=self.timeout
        )

    def delete(self, endpoint, headers=None):
        return requests.delete(
            "{}{}".format(self.base_url, endpoint),
            headers=headers,
            timeout=self.timeout
        )
