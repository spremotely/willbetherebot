from models import State
from data.staterepo import StateRepo


class AlchemyStateRepo(StateRepo):

    def __init__(self, context):
        super().__init__(context)

    def get_state(self, chat_id, user_id):
        return self._context.get_context().query(State).filter_by(chat_id=chat_id, user_id=user_id).first()

    def create_state(self, chat, user, message_id, command, state_value, entity):
        state = State(message_id, command, state_value)
        self._context.get_context().add(state)
        state.chat = chat
        state.user = user
        state.entity = entity
        self._context.get_context().flush()
        self._context.get_context().refresh(state)
        return state

    def update_state(self, state_id, command, state_value, entity=None):
        state = self._context.get_context().query(State).filter_by(id=state_id).first()

        if not state:
            return

        state.command = command
        state.state = state_value
        state.entity = entity

        return state
