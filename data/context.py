from abc import ABC, abstractmethod


class Context(ABC):

    @abstractmethod
    def create_context(self):
        pass

    @abstractmethod
    def get_context(self):
        pass

    @abstractmethod
    def save_changes(self):
        pass

    @abstractmethod
    def close(self):
        pass
