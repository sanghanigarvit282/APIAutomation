import pytest

from constants.constants import CREATE_BOOKING
from helpers.common_helper import validate_response_fields, validate_booking_business_data, \
    validate_200_ok_status_code, validate_201_status_code, validate_404_status_code
from helpers.payload_builder import build_custom_payload
from jsonData.payload import CREATE_BOOKING_DATA, CREATE_BOOKING_FIXTURE_DATA


@pytest.mark.parametrize(
    "firstname,lastname,price",
    CREATE_BOOKING_DATA
)
def test_create_booking(api_client, firstname, lastname, price):
    payload = build_custom_payload(firstname,lastname,price)
    response = api_client.post(CREATE_BOOKING, json=payload)
    validate_200_ok_status_code(response.status_code, current_operation="for booking creation")
    body = response.json()
    assert "bookingid" in body, (
        f"'bookingid' missing in create booking response. Response: {body}"
    )
    assert body["bookingid"] is not None, "bookingid is None in response"

    validate_response_fields(payload, body["booking"])
    errors = validate_booking_business_data(payload, body["booking"])
    assert not errors, "Booking validation failed:\n" + "\n".join(errors)


@pytest.mark.parametrize(
    "create_booking_fixture",
    CREATE_BOOKING_FIXTURE_DATA,
    indirect=True
)
def test_get_booking(api_client, create_booking_fixture):
    booking_id, expected_payload = create_booking_fixture
    get_resp = api_client.get("{}/{}".format(CREATE_BOOKING,booking_id))
    validate_200_ok_status_code(get_resp.status_code,
                                current_operation=f"when fetching booking {booking_id}")
    errors = validate_booking_business_data(expected_payload, get_resp.json())
    assert not errors, "Booking validation failed:\n" + "\n".join(errors)

@pytest.mark.parametrize(
    "create_booking_fixture",
    CREATE_BOOKING_FIXTURE_DATA,
    indirect=True
)
@pytest.mark.parametrize("updated_firstname", ["Chris"])
def test_update_booking(api_client, auth_headers, create_booking_fixture, updated_firstname):
    booking_id, expected_payload = create_booking_fixture
    payload = build_custom_payload(firstname=updated_firstname)
    update_resp = api_client.put(
        "{}/{}".format(CREATE_BOOKING,booking_id),
        json=payload,
        headers=auth_headers
    )
    validate_200_ok_status_code(update_resp.status_code,
                                current_operation=f"when updating booking {booking_id}")

    assert update_resp.json().get("firstname") == updated_firstname, (
        f"Booking firstname was not updated correctly.\n"
        f"Expected: {updated_firstname}\n"
        f"Actual: {update_resp.json().get('firstname')}"
    )

    errors = validate_booking_business_data(payload, update_resp.json())
    assert not errors, "Booking validation failed:\n" + "\n".join(errors)


@pytest.mark.parametrize(
    "create_booking_fixture",
    CREATE_BOOKING_FIXTURE_DATA,
    indirect=True
)
def test_delete_booking(api_client, create_booking_fixture, auth_headers):
    booking_id, expected_payload = create_booking_fixture

    delete_resp = api_client.delete(
        "{}/{}".format(CREATE_BOOKING,booking_id),
        headers=auth_headers
    )
    validate_201_status_code(delete_resp.status_code, booking_id)

    get_resp = api_client.get(
        "{}/{}".format(CREATE_BOOKING, booking_id)
    )
    validate_404_status_code(get_resp.status_code, booking_id)
