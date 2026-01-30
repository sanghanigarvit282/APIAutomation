import pytest

from constants.constants import CREATE_BOOKING
from helpers.payload_builder import build_custom_payload
from lib.custom_exception import CustomException


@pytest.fixture
def create_booking_fixture(api_client, request):
    payload = build_custom_payload(request.param["firstname"],
                                   request.param["lastname"],
                                   request.param["totalprice"])
    api_resp = api_client.post(f"{CREATE_BOOKING}", json=payload)
    if "bookingid" not in api_resp.json():
        raise CustomException("Booking id not found. API response '{}'".format(api_resp.text))
    booking_id = api_resp.json()["bookingid"]
    return booking_id, payload
