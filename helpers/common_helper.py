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
