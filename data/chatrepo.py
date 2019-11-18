from abc import abstractmethod

from data.repo import Repo


class ChatRepo(Repo):

    @abstractmethod
    def get_chat(self, chat_id):
        pass

    @abstractmethod
    def create_chat(self, chat_id, chat_type):
        pass
