from abc import abstractmethod

from data.repo import Repo


class PhotoRepo(Repo):

    @abstractmethod
    def create_photo(self, uri):
        pass

    @abstractmethod
    def get_photo(self, photo_id):
        pass
