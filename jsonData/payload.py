booking_payload = {
    "firstname": str,
    "lastname": str,
    "totalprice": int,
    "depositpaid": bool,
    "bookingdates": dict,
    "additionalneeds": str
}

sample_booking_payload = {
    "firstname": "Garvit",
    "lastname": "Sanghani",
    "totalprice": 233,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2024-01-01",
        "checkout": "2024-01-05"
    },
    "additionalneeds": "Breakfast"
}
