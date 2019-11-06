from abc import ABC, abstractmethod


class Scenario(ABC):

    _next_scenario: None

    @abstractmethod
    def set_next(self, scenario):
        self._next_scenario = scenario
        return scenario

    @abstractmethod
    def handle(self, chat, user, message):
        if self._next_scenario:
            return self._next_scenario.handle(chat, user, message)

        return None
