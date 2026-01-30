import logging

class CustomException(Exception):
    def __init__(self, message):
        logging.error(message)