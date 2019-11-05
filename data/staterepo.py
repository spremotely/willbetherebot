from abc import ABC, abstractmethod


class StateRepo(ABC):

    @abstractmethod
    def get_state(self, chat_id, user_id):
        pass

    @abstractmethod
    def create_state(self, chat, user, message_id, command, state, entity=None):
        pass

