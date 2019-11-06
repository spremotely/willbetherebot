from models import State
from data.staterepo import StateRepo


class AlchemyStateRepo(StateRepo):

    def __init__(self, context):
        self.__session = context.get_context()

    def get_state(self, chat_id, user_id):
        return self.__session.query(State).filter_by(chat_id=chat_id, user_id=user_id).first()

    def create_state(self, chat, user, message_id, command, state_value, entity=None):
        state = State(chat, user, message_id, command, state_value, entity)
        self.__session.add(state)
        return state

    def update_state(self, state_id, command, state_value, entity=None):
        state = self.__session.query(State).filter_by(id=state_id).first()

        if not state:
            return

        state.command = command
        state.state = state_value
        state.entity = entity

        return state
