from data.chatrepo import ChatRepo
from data.models import Chat


class AlchemyChatRepo(ChatRepo):

    def __init__(self, context):
        super().__init__(context)

    def get_chat(self, chat_id):
        return self._context.get_context().query(Chat).filter_by(id=chat_id).first()

    def create_chat(self, chat_id, chat_type):
        chat = Chat(chat_id, chat_type)
        self._context.get_context().add(chat)
        self._context.get_context().flush()
        self._context.get_context().refresh(chat)
        return chat
