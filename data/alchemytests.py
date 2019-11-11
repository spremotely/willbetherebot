import os
import unittest

from data.alchemychatrepo import AlchemyChatRepo
from data.alchemycontext import AlchemyContext
from data.alchemyentityrepo import AlchemyEntityRepo
from data.alchemychatstaterepo import AlchemyChatStateRepo
from data.alchemyuserrepo import AlchemyUserRepo
from models import User, Chat, ChatState, Entity


class FakeUser:

    def __init__(
            self,
            user_id,
            user_name,
            first_name,
            last_name,
            is_bot,
            state):
        self.id = user_id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.is_bot = is_bot
        self.state = state

    def __eq__(self, other):
        return other.id == self.id and \
            other.user_name == self.user_name and \
            other.first_name == self.first_name and \
            other.last_name == self.last_name and \
            other.is_bot == self.is_bot


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
        self.user = FakeUser(1, "user name", "first name", "last name", False, None)

    def test_create_user(self):
        user = self.user_repo.create_user(
            self.user.id,
            self.user.user_name,
            self.user.first_name,
            self.user.last_name)
        print(user, self.user)
        self.assertEqual(user, self.user)

    def test_get_user(self):
        user = self.user_repo.get_user(self.user.id)
        self.assertEqual(user, self.user)


class AlchemyEntityRepoTest(AlchemyRepo):

    def setUp(self):
        self.entity_repo = AlchemyEntityRepo(self.context)
        self.entity = Entity(10, "photo")
        self.entity.id = 1

    def test_create_entity(self):
        entity = self.entity_repo.create_entity(
            self.entity.entity_id, self.entity.entity_type)
        self.assertEqual(entity, self.entity)


class AlchemyStateRepoTest(AlchemyRepo):

    def setUp(self):
        self.chat_repo = AlchemyChatRepo(self.context)
        self.user_repo = AlchemyUserRepo(self.context)
        self.entity_repo = AlchemyEntityRepo(self.context)
        self.state_repo = AlchemyChatStateRepo(self.context)
        self.chat = self.chat_repo.create_chat(10, "private")
        self.user = self.user_repo.create_user(
            20,
            "user name",
            "first name",
            "last name")
        self.entity = self.entity_repo.create_entity(
            30, "photo")

    def test_create_state(self):
        state = self.state_repo.create_state(
            self.chat,
            self.user,
            40,
            "add",
            "welcome",
            self.entity)
        with self.subTest(state=state):
            self.assertEqual(state.chat_id, self.chat.id)
        with self.subTest(state=state):
            self.assertEqual(state.user_id, self.user.id)
        with self.subTest(state=state):
            self.assertEqual(state.entity_id, self.entity.id)
        with self.subTest(state=state):
            self.assertEqual(state.id, 1)
