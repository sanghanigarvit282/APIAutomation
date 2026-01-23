import pytest
from jsonData import payload as p

@pytest.fixture
def create_booking_fixture(api_client, request):
    payload = p.booking_payload.copy()
    payload.update(request.param)
    return api_client.post("/booking", json=payload), payload
