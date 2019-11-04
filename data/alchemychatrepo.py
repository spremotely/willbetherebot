from data.chatrepo import ChatRepo
from models import Chat


class AlchemyChatRepo(ChatRepo):

    def __init__(self, context):
        self.__session = context.get_context()

    def get_chat(self, chat_id):
        return self.__session.query(Chat).filter_by(id=chat_id).first()

    def create_chat(self, chat_id, chat_type):
        chat = Chat(chat_id, chat_type)
        self.__session.add(Chat(chat_id, chat_type))
        return chat
