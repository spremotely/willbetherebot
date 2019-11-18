from abc import abstractmethod

from data.repo import Repo


class EntityRepo(Repo):

    @abstractmethod
    def create_entity(self, entity_id, entity_type):
        pass
