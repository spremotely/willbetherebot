import re
from abc import ABC, abstractmethod


class Scenario(ABC):

    @abstractmethod
    def __init__(self, scenario=None):
        self._scenario = scenario

    @abstractmethod
    def handle(self, chat, user, state, message):
        if self._scenario:
            return self._scenario.handle(chat, user, state, message)

        return

    @staticmethod
    def is_command(message, command=None, pattern=None):
        if not command:
            return message.content_type == "text" and message.text.startswith("/")

        if not pattern:
            return message.content_type == "text" and message.text.startswith(f"/{command}")

        return re.match(f"/{command} {pattern}", message.text)

    @staticmethod
    def is_text(message):
        return message.content_type == "text"

    @staticmethod
    def is_location(message):
        return message.content_type == "location"

    @staticmethod
    def is_photo(message):
        return message.content_type == "photo"

    @staticmethod
    def get_number(message, command, pattern):
        return re.search(f"/{command} ({pattern})", message.text).group(1)
