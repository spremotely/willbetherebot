import os
import unittest

from data.alchemychatrepo import AlchemyChatRepo
from data.alchemycontext import AlchemyContext
from data.alchemyuserrepo import AlchemyUserRepo
from models import User


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

    def test_create_chat(self):
        chat = self.chat_repo.create_chat(1, "test")
        self.assertEqual(chat.id, 1)

    def test_get_chat(self):
        chat = self.chat_repo.get_chat(1)
        self.assertIsNotNone(chat)


class AlchemyUserRepoTest(AlchemyRepo):

    def setUp(self):
        self.user_repo = AlchemyUserRepo(self.context)
        self.user = User(1, "user name", "first name", "last name")

    def test_create_user(self):
        user = self.user_repo.create_user(self.user.id, self.user.user_name, self.user.first_name, self.user.last_name)
        self.assertEqual(user, self.user)

    def test_get_user(self):
        user = self.user_repo.get_user(self.user.id)
        self.assertEqual(user, self.user)
