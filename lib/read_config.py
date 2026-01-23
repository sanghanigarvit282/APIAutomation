"""
Provides a singleton-based configuration reader for loading and accessing
application configuration values from a config.ini file.


The ConfigReader ensures that the configuration file is loaded only once
and shared across the entire test framework. It also supports runtime
overrides of configuration values
"""

import configparser
import os
from lib.custom_exception import CustomException


class ConfigReader:
    """
    Config reader class. Reads config file and provides value of the config key as class property
    Singleton class responsible for reading and providing configuration values from a config.ini file.
    """
    _instance = None
    _config = None
    _overrides = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """
        Loads the configuration values from the config.ini file.

        Reads the config.ini file from the project root directory and
        stores the parsed data internally. Raises a CustomException if
        the configuration file is not found.
        :return:
        """
        self._config = configparser.ConfigParser()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config.ini")

        if not os.path.exists(config_path):
            raise CustomException("Config file not found at {}".format(config_path))

        # This will load config file data in _config variable
        self._config.read(config_path)

    def set_override(self, key, value):
        self._overrides[key] = value

    def get(self, key):
        if key in self._overrides:
            return self._overrides[key]

        return self._config["DEFAULT"].get(key)

    # Specific variable getter methods
    def get_url(self):
        return self.get("url")

    def get_username(self):
        return self.get("username")

    def get_password(self):
        return self.get("password")