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
