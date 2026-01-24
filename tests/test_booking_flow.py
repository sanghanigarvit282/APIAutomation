import pytest

from helpers.common_helper import validate_response_fields
from jsonData import payload as p


@pytest.mark.parametrize("firstname,lastname,price", [
    ("John","Wick", 100),
    ("Alice","Wonder", 200)
])
def test_create_booking(api_client, firstname, lastname, price):
    payload = p.booking_payload.copy()
    payload.update({
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": price
    })

    response = api_client.post("/booking", json=payload)

    assert response.status_code == 200, (
        f"Expected status code 200 for booking creation, "
        f"but got {response.status_code}. Response: {response.text}"
    )

    body = response.json()

    assert "bookingid" in body, (
        f"'bookingid' missing in create booking response. Response: {body}"
    )

    assert body["bookingid"] is not None, (
        "bookingid is None in create booking response"
    )

    validate_response_fields(payload, body["booking"])

    assert payload == body["booking"], (
        f"Created booking does not match request payload.\n"
        f"Expected: {payload}\n"
        f"Actual: {body['booking']}"
    )


@pytest.mark.parametrize(
    "create_booking_fixture",
    [
        {"firstname": "John", "lastname": "Wick", "totalprice": 100}
    ],
    indirect=True
)
def test_get_booking(api_client, create_booking_fixture):
    booking_response, expected_payload = create_booking_fixture
    booking_id = booking_response.json()["bookingid"]

    get_resp = api_client.get(f"/booking/{booking_id}")

    assert get_resp.status_code == 200, (
        f"Expected status code 200 when fetching booking {booking_id}, "
        f"but got {get_resp.status_code}. Response: {get_resp.text}"
    )

    assert expected_payload == get_resp.json(), (
        f"Fetched booking data does not match expected payload.\n"
        f"Expected: {expected_payload}\n"
        f"Actual: {get_resp.json()}"
    )


@pytest.mark.parametrize(
    "create_booking_fixture",
    [
        {"firstname": "John", "lastname": "Wick", "totalprice": 100}
    ],
    indirect=True
)
@pytest.mark.parametrize("updated_firstname", ["Chris"])
def test_update_booking(api_client, auth_headers, create_booking_fixture, updated_firstname):
    booking_response, _ = create_booking_fixture
    booking_id = booking_response.json()["bookingid"]

    payload = p.booking_payload.copy()
    payload["firstname"] = updated_firstname

    update_resp = api_client.put(
        "/booking/{}".format(booking_id),
        json=payload,
        headers=auth_headers
    )

    assert update_resp.status_code == 200, (
        f"Expected status code 200 when updating booking {booking_id}, "
        f"but got {update_resp.status_code}. Response: {update_resp.text}"
    )

    assert update_resp.json().get("firstname") == updated_firstname, (
        f"Booking firstname was not updated correctly.\n"
        f"Expected: {updated_firstname}\n"
        f"Actual: {update_resp.json().get('firstname')}"
    )


@pytest.mark.parametrize(
    "create_booking_fixture",
    [
        {"firstname": "John", "lastname": "Wick", "totalprice": 100}
    ],
    indirect=True
)
def test_delete_booking(api_client, create_booking_fixture, auth_headers):
    booking_response, _ = create_booking_fixture
    booking_id = booking_response.json()["bookingid"]

    delete_resp = api_client.delete(
        "/booking/{}".format(booking_id),
        headers=auth_headers
    )

    assert delete_resp.status_code == 201, (
        f"Expected status code 201 when deleting booking {booking_id}, "
        f"but got {delete_resp.status_code}. Response: {delete_resp.text}"
    )

    get_resp = api_client.get(
        f"/booking/{booking_id}"
    )

    assert get_resp.status_code == 404, (
        f"Deleted booking {booking_id} should not exist, "
        f"but GET returned {get_resp.status_code}. Response: {get_resp.text}"
    )
