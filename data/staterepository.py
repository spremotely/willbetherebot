from abc import ABC, abstractmethod


class StateRepository(ABC):

    @abstractmethod
    def get_state(self, chat_id, user_id):
        pass

