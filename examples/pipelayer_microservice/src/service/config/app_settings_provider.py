import os

from yaml import safe_load


class AppSettingsProvider:
    def __init__(self, env: str) -> None:
        self.env = env

    def get(self) -> dict:
        cwd = os.path.dirname(__file__)
        with open(f"{cwd}/app_settings.yaml", "r") as f:
            environments: dict = safe_load(f.read())
        return environments.get(self.env)
