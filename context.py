from abc import ABC, abstractmethod


class Context(ABC):

    @abstractmethod
    def get_context(self):
        pass
