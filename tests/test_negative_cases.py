import pytest

from constants.constants import CREATE_BOOKING, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED
from helpers.payload_builder import build_custom_payload
from jsonData.payload import CREATE_BOOKING_FIXTURE_DATA


def test_get_non_existing_booking(api_client):
    response = api_client.get("{}/99999999".format(CREATE_BOOKING))

    assert response.status_code == HTTP_404_NOT_FOUND, (
        "Expected 404 when fetching non-existing booking, "
        "but got {}. Response: {}".format(response.status_code,response.text)
    )

@pytest.mark.parametrize(
    "create_booking_fixture",
    CREATE_BOOKING_FIXTURE_DATA,
    indirect=True
)
@pytest.mark.parametrize("updated_firstname", ["Chris"])
def test_update_booking_without_auth(api_client, auth_headers, create_booking_fixture, updated_firstname):
    booking_id, expected_payload = create_booking_fixture

    payload = build_custom_payload(firstname=updated_firstname)
    response = api_client.put("{}/{}".format(CREATE_BOOKING,booking_id), json=payload)

    assert response.status_code == HTTP_403_FORBIDDEN, (
        "Expected 403 Forbidden when updating booking without auth, "
        "but got {}. Response: {}".format(response.status_code,response.text)
    )


def test_delete_invalid_booking(api_client, auth_headers):
    response = api_client.delete(
        "{}/99999999".format(CREATE_BOOKING),
        headers=auth_headers
    )

    assert response.status_code in (HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED), (
        "Expected 404 or 405 when deleting invalid booking, "
        "but got {}. Response: {}".format(response.status_code,response.text)
    )
