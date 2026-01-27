from jsonData import payload as p

def build_custom_payload(firstname="", lastname="", price=""):
    """
    Builds the payload schema.
    This will fetch sample json schema from payload.py
    Currently, I have made firstname, lastname and price values dynamic
    Remaining values are hard coded for now.
    :param firstname: value from parameterized test
    :param lastname: value from parameterized test
    :param price: value from parameterized test
    :return: {dict} Updated payload schema
    """
    if not firstname:
        firstname = p.sample_booking_payload["firstname"]
    if not lastname:
        lastname = p.sample_booking_payload["lastname"]
    if not price:
        price = p.sample_booking_payload["totalprice"]
    payload = p.booking_payload.copy()
    payload.update({
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": price,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-05"
        },
        "additionalneeds": "No"
    })
    return payload