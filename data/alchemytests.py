import os
import unittest

from data.alchemychatrepo import AlchemyChatRepo
from data.alchemycontext import AlchemyContext
from data.alchemystaterepo import AlchemyStateRepo
from data.alchemyuserrepo import AlchemyUserRepo
from models import User, Chat, ChatState, Entity


class AlchemyRepo(unittest.TestCase):

    db_filename = "test.db"
    context = None

    @classmethod
    def setUpClass(cls):
        cls.context = AlchemyContext(f"sqlite:///{cls.db_filename}")

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        os.remove(cls.db_filename)


class AlchemyChatRepoTest(AlchemyRepo):

    def setUp(self):
        self.chat_repo = AlchemyChatRepo(self.context)
        self.chat = Chat(1, "private")

    def test_create_chat(self):
        chat = self.chat_repo.create_chat(self.chat.id, self.chat.type)
        self.assertEqual(chat, self.chat)

    def test_get_chat(self):
        chat = self.chat_repo.get_chat(self.chat.id)
        self.assertEqual(chat, self.chat)


class AlchemyUserRepoTest(AlchemyRepo):

    def setUp(self):
        self.user_repo = AlchemyUserRepo(self.context)
        self.user = User(1, "user name", "first name", "last name")

    def test_create_user(self):
        user = self.user_repo.create_user(
            self.user.id,
            self.user.user_name,
            self.user.first_name,
            self.user.last_name)
        self.assertEqual(user, self.user)

    def test_get_user(self):
        user = self.user_repo.get_user(self.user.id)
        self.assertEqual(user, self.user)


class AlchemyStateRepoTest(AlchemyRepo):

    def setUp(self):
        self.state_repo = AlchemyStateRepo(self.context)
        self.chat = Chat(10, "private")
        self.user = User(20, "user name", "first name", "last name")
        self.entity = Entity(30, "photo")
        self.state = ChatState(30, "add", "welcome")
        self.state.chat = self.chat
        self.state.user = self.user
        self.state.entity = self.entity

    def test_create_state(self):
        state = self.state_repo.create_state(
            self.chat,
            self.user,
            self.state.message_id,
            self.state.command,
            self.state.state,
            self.entity)
        print(state)
