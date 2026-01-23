"""
It contains functions for raising different exceptions
"""

import logging


class CustomException(Exception):
    """
    Custom class for Exception
    """
    def __init__(self, message):
        """
        :param message: Custom Exception message
        """
        logging.error(message)