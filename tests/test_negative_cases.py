def test_get_non_existing_booking(api_client):
    response = api_client.get("/booking/99999999")

    assert response.status_code == 404, (
        "Expected 404 when fetching non-existing booking, "
        "but got {}. Response: {}".format(response.status_code,response.text)
    )


def test_update_booking_without_auth(api_client):
    response = api_client.put("/booking/1", json={
        "firstname": "Hacker"
    })

    assert response.status_code == 403, (
        "Expected 403 Forbidden when updating booking without auth, "
        "but got {}. Response: {}".format(response.status_code,response.text)
    )


def test_delete_invalid_booking(api_client, auth_headers):
    response = api_client.delete(
        "/booking/99999999",
        headers=auth_headers
    )

    assert response.status_code in (404, 405), (
        "Expected 404 or 405 when deleting invalid booking, "
        "but got {}. Response: {}".format(response.status_code,response.text)
    )

