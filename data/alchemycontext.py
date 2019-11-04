from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.context import Context


class AlchemyContext(Context):

    def __init__(self, connection_string):
        self.__engine = create_engine(connection_string)
        self.__session = sessionmaker(bind=self.__engine)()

    def get_context(self):
        return self.__session

    def save_changes(self):
        self.__session.commit()
