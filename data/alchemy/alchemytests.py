import os
import unittest

from data.alchemy.alchemychatrepo import AlchemyChatRepo
from data.alchemy.alchemychatstaterepo import AlchemyChatStateRepo
from data.alchemy.alchemycontext import AlchemyContext
from data.alchemy.alchemyentityrepo import AlchemyEntityRepo
from data.alchemy.alchemyphotorepo import AlchemyPhotoRepo
from data.alchemy.alchemyuserrepo import AlchemyUserRepo


class FakeChat:

    def __init__(self, pk, chat_type):
        self.id = pk
        self.type = chat_type

    def __eq__(self, other):
        return other.id == self.id and other.type == self.type


class FakeUser:

    def __init__(
            self,
            user_id,
            user_name,
            first_name,
            last_name,
            is_bot):
        self.id = user_id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.is_bot = is_bot

    def __eq__(self, other):
        return other.id == self.id and \
            other.user_name == self.user_name and \
            other.first_name == self.first_name and \
            other.last_name == self.last_name and \
            other.is_bot == self.is_bot


class FakeEntity:

    def __init__(self, pk, entity_id, entity_type):
        self.id = pk
        self.entity_id = entity_id
        self.entity_type = entity_type

    def __eq__(self, other):
        return other.id == self.id and other.entity_id == self.entity_id and other.entity_type == self.entity_type


class FakeChatState:

    def __init__(
            self,
            state_id,
            chat,
            user,
            message_id,
            entity,
            command,
            state_value):
        self.id = state_id
        self.chat = chat
        self.chat_id = chat.id
        self.user = user
        self.user_id = user.id
        self.entity = entity
        self.entity_id = entity.id
        self.message_id = message_id
        self.command = command
        self.state = state_value

    def __eq__(self, other):
        return other.id == self.id and \
            other.chat_id == self.chat_id and \
            other.user_id == self.user_id and \
            other.entity_id == self.entity_id and \
            other.message_id == self.message_id and \
            other.command == self.command


class FakePhoto:

    def __init__(self, pk, uri):
        self.id = pk
        self.uri = uri

    def __eq__(self, other):
        return other.id == self.id and other.uri == self.uri


class AlchemyRepoTest(unittest.TestCase):

    db_filename = "test.db"
    context = None

    @classmethod
    def setUpClass(cls):
        cls.context = AlchemyContext(f"sqlite:///{cls.db_filename}")

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        os.remove(cls.db_filename)


class AlchemyChatRepoTest(AlchemyRepoTest):

    def setUp(self):
        self.chat_repo = AlchemyChatRepo(self.context)
        self.chat = FakeChat(1, "private")

    def test_create_chat(self):
        chat = self.chat_repo.create_chat(self.chat.id, self.chat.type)
        self.assertEqual(chat, self.chat)

    def test_get_chat(self):
        chat = self.chat_repo.get_chat(self.chat.id)
        self.assertEqual(chat, self.chat)


class AlchemyUserRepoTest(AlchemyRepoTest):

    def setUp(self):
        self.user_repo = AlchemyUserRepo(self.context)
        self.user = FakeUser(
            1,
            "user name",
            "first name",
            "last name",
            False)

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


class AlchemyEntityRepoTest(AlchemyRepoTest):

    def setUp(self):
        self.entity_repo = AlchemyEntityRepo(self.context)
        self.entity = FakeEntity(1, 10, "photo")
        self.entity.id = 1

    def test_create_entity(self):
        entity = self.entity_repo.create_entity(
            self.entity.entity_id, self.entity.entity_type)
        self.assertEqual(entity, self.entity)


class AlchemyStateRepoTest(AlchemyRepoTest):

    def setUp(self):
        self.chat_repo = AlchemyChatRepo(self.context)
        self.user_repo = AlchemyUserRepo(self.context)
        self.entity_repo = AlchemyEntityRepo(self.context)
        self.state_repo = AlchemyChatStateRepo(self.context)

        self.fake_chat = FakeChat(1, "private")
        self.fake_user = FakeUser(
            1,
            "user name",
            "first name",
            "last name",
            False)
        self.fake_entity = FakeEntity(1, 10, "photo")
        self.fake_entity_update = FakeEntity(2, 11, "location")
        self.fake_state = FakeChatState(
            1,
            self.fake_chat,
            self.fake_user,
            20,
            self.fake_entity,
            "add",
            "welcome")
        self.fake_state_update = FakeChatState(
            1,
            self.fake_chat,
            self.fake_user,
            30,
            self.fake_entity_update,
            "add",
            "location")

    def test_create_state(self):
        chat = self.chat_repo.create_chat(1, "private")
        user = self.user_repo.create_user(
            1,
            "user name",
            "first name",
            "last name")
        entity = self.entity_repo.create_entity(
            10, "photo")

        state = self.state_repo.create_state(
            chat,
            user,
            20,
            "add",
            "welcome",
            entity)
        with self.subTest(state=state):
            self.assertEqual(state, self.fake_state)
        with self.subTest(state=state):
            self.assertIsNotNone(state.updated_at)

    def test_get_state(self):
        state = self.state_repo.get_state(self.fake_chat.id, self.fake_user.id)
        self.assertEqual(state, self.fake_state)

    def test_update_state(self):
        entity = self.entity_repo.create_entity(11, "location")
        state = self.state_repo.update_state(
            self.fake_state.id, "add", "location", 30, entity)
        self.assertEqual(state, self.fake_state_update)


class AlchemyPhotoRepoTest(AlchemyRepoTest):

    def setUp(self):
        self.photo_repo = AlchemyPhotoRepo(self.context)
        self.fake_photo = FakePhoto(1, "test photo")

    def test_create_photo(self):
        photo = self.photo_repo.create_photo(self.fake_photo.uri)
        self.assertEqual(photo, self.fake_photo)

    def test_get_photo(self):
        photo = self.photo_repo.get_photo(self.fake_photo.id)
        self.assertEqual(photo, self.fake_photo)
