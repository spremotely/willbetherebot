from abc import ABC, abstractmethod


class UserRepo(ABC):

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def create_user(self, user_id, user_name, first_name, last_name, is_bot=False):
        pass
