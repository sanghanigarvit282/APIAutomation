import pytest

from constants.constants import CREATE_BOOKING
from jsonData import payload as p

@pytest.fixture
def create_booking_fixture(api_client, request):
    payload = p.sample_booking_payload.copy()
    payload.update(request.param)
    return api_client.post(f"{CREATE_BOOKING}", json=payload), payload
