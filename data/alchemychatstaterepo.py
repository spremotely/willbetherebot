from models import ChatState
from data.chatstaterepo import ChatStateRepo


class AlchemyChatStateRepo(ChatStateRepo):

    def __init__(self, context):
        super().__init__(context)

    def get_state(self, chat_id, user_id):
        return self._context.get_context().query(ChatState).filter_by(chat_id=chat_id, user_id=user_id).first()

    def create_state(self, chat, user, message_id, command, state_value, entity=None):
        state = ChatState(chat, user, message_id, command, state_value, entity)
        self._context.get_context().add(state)
        self._context.get_context().flush()
        self._context.get_context().refresh(state)
        return state

    def update_state(self, state_id, command, state_value, entity=None):
        state = self._context.get_context().query(ChatState).filter_by(id=state_id).first()

        if not state:
            return

        state.command = command
        state.state = state_value
        state.entity = entity

        return state
