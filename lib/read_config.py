import configparser
import logging
from pathlib import Path


class ConfigReader:
    def __init__(self, env="dev"):
        self.env = env
        self._config = configparser.ConfigParser()
        config_path = Path.cwd() / "config.ini"
        if not config_path.exists():
            raise FileNotFoundError(f"config.ini not found at {config_path}")
        self._config.read(config_path)
        if env not in self._config:
            raise ValueError(f"Environment '{env}' not found in config.ini")
        logging.info(
            "Using env='%s', url='%s', username='%s', password='%s'",
            self.env,
            self.get("url"),
            self.get("username"),
            self.get("password")
        )

    def get(self, key):
        return self._config[self.env].get(key)

    def get_url(self):
        return self.get("url")

    def get_username(self):
        return self.get("username")

    def get_password(self):
        return self.get("password")

