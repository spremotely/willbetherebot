from abc import ABC, abstractmethod


class Repo(ABC):

    @abstractmethod
    def __init__(self, context):
        self._context = context
