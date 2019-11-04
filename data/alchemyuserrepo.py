from data.userrepo import UserRepo
from models import User


class AlchemyUserRepo(UserRepo):

    def __init__(self, context):
        self.__session = context.get_context()

    def get_user(self, user_id):
        self.__session.query(User).filter_by(user_id=user_id).first()

    def create_user(self, user_name, first_name, last_name, is_bot=False):
        self.__session.add(User(user_name, first_name, last_name, is_bot))
