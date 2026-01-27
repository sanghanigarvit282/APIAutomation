import logging

from constants.constants import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from lib.custom_exception import CustomException


def validate_response_fields(expected_response, actual_response):
    """
    This method validates expected response schema with API response
    :param expected_response: {dict}
    :param actual_response: {dict}
    :return: None
    """
    missing_parameters = []
    for keys in expected_response.keys():
        if keys not in actual_response:
            missing_parameters.append(keys)
    if missing_parameters:
        raise CustomException("Important response fields are not present. "
                              "Missing parameters are '{}'".format(missing_parameters))


def validate_booking_business_data(expected_payload, actual_response):
    """
    This method validates all key values from expected schema to actual API response
    :param expected_payload: {dict}
    :param actual_response: {dict}
    :return: [list] containing mismatched keys, values
    """
    mismatched_data = []
    logging.info("Expected schema '{}', API Response'{}'".format(expected_payload, actual_response))

    for key, expected_value in expected_payload.items():
        if key not in actual_response:
            mismatched_data.append(f"Missing key in actual booking: '{key}'")
            continue

        actual_value = actual_response[key]

        if actual_value != expected_value:
            mismatched_data.append(
                f"Mismatch for key '{key}': "
                f"expected '{expected_value}', got '{actual_value}'"
            )

    return mismatched_data

def validate_200_ok_status_code(response_status_code, current_operation):
    assert response_status_code == HTTP_200_OK, (
        f"Expected status code 200 {current_operation}, "
        f"but got {response_status_code}."
    )

def validate_201_status_code(response_status_code, booking_id):
    assert response_status_code == HTTP_201_CREATED, (
        f"Expected status code 201 when deleting booking {booking_id}, "
        f"but got {response_status_code}."
    )

def validate_404_status_code(response_status_code, booking_id):
    assert response_status_code == HTTP_404_NOT_FOUND, (
        f"Deleted booking {booking_id} should not exist, "
        f"but GET returned {response_status_code}."
    )