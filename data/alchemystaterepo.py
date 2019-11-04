from models import State
from data.staterepo import StateRepo


class AlchemyStateRepo(StateRepo):

    def __init__(self, context):
        self.__session = context.get_context()

    def get_state(self, chat_id, user_id):
        return self.__session.query(State).filter_by(chat_id=chat_id, user_id=user_id).first()
