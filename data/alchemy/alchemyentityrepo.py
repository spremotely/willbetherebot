from data.entityrepo import EntityRepo
from data.models import Entity


class AlchemyEntityRepo(EntityRepo):

    def __init__(self, context):
        super().__init__(context)

    def create_entity(self, entity_id, entity_type):
        entity = Entity(entity_id, entity_type)
        self._context.get_context().add(entity)
        self._context.get_context().flush()
        self._context.get_context().refresh(entity)
        return entity
