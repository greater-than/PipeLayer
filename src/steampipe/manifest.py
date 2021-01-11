from collections import OrderedDict
from datetime import datetime


class Manifest(OrderedDict):
    def add_entry(self, message: str) -> None:
        self.update({datetime.now(): message})
