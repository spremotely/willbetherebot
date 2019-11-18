from data.userrepo import UserRepo
from data.models import User


class AlchemyUserRepo(UserRepo):

    def __init__(self, context):
        super().__init__(context)

    def get_user(self, user_id):
        return self._context.get_context().query(User).filter_by(id=user_id).first()

    def create_user(self, user_id, user_name, first_name, last_name, is_bot=False):
        user = User(user_id, user_name, first_name, last_name, is_bot)
        self._context.get_context().add(user)
        self._context.get_context().flush()
        self._context.get_context().refresh(user)
        return user
