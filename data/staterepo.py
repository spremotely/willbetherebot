from abc import ABC, abstractmethod


class StateRepo(ABC):

    @abstractmethod
    def get_state(self, chat_id, user_id):
        pass

    @abstractmethod
    def create_state(self, chat, user, message_id, command, state_value, entity=None):
        pass

    @abstractmethod
    def update_state(self, state_id, command, state_value, entity=None):
        pass
