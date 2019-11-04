from abc import ABC, abstractmethod


class ChatRepo(ABC):

    @abstractmethod
    def get_chat(self, chat_id):
        pass

    @abstractmethod
    def create_chat(self, chat_id, chat_type):
        pass
