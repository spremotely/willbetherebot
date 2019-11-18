from abc import abstractmethod

from data.repo import Repo


class LocationRepo(Repo):

    @abstractmethod
    def create_location(self, chat, user, photo, longitude, latitude):
        pass

    @abstractmethod
    def get_locations(self, chat_id, user_id, limit=None):
        pass
