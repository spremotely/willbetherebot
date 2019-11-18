from data.locationrepo import LocationRepo
from data.models import Location


class AlchemyLocationRepo(LocationRepo):

    def __init__(self, context):
        super().__init__(context)

    def create_location(self, chat, user, photo, longitude, latitude):
        location = Location(chat, user, photo, longitude, latitude)
        self._context.get_context().add(location)
        self._context.get_context().flush()
        self._context.get_context().refresh(location)
        return location

    def get_locations(self, chat_id, user_id, limit=None):
        if not limit:
            return self._context.get_context().query(Location).filter_by(
                chat_id=chat_id, user_id=user_id).all()

        return self._context.get_context().query(Location).filter_by(
            chat_id=chat_id, user_id=user_id).limit(limit).all()
