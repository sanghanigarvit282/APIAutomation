import requests

class APIClient:
    """
    A simple HTTP API client wrapper around the requests library.
    This client provides methods for common HTTP methods
    (GET, POST, PUT, DELETE) with a configurable base URL and timeout.
    """

    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout

    def _build_url(self, endpoint: str) -> str:
        return "{}/{}".format(self.base_url.rstrip('/'),endpoint.lstrip('/'))

    def _request(self, method: str, endpoint: str, **kwargs):
        url = self._build_url(endpoint)
        response = requests.request(
            method=method,
            url=url,
            timeout=self.timeout,
            **kwargs
        )
        return response

    def get(self, endpoint, params=None, headers=None):
        return self._request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint, json=None, headers=None):
        return self._request("POST", endpoint, json=json, headers=headers)

    def put(self, endpoint, json=None, headers=None):
        return self._request("PUT", endpoint, json=json, headers=headers)

    def delete(self, endpoint, headers=None):
        return self._request("DELETE", endpoint, headers=headers)

