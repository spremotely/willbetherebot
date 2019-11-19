from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from data.context import Context
from data.models import Base


class AlchemyContext(Context):

    def __init__(self, connection_string):
        engine = create_engine(connection_string)
        Base.metadata.create_all(engine)
        self.__Session = scoped_session(sessionmaker(bind=engine))
        self.__session = None

    def create_context(self):
        self.__session = self.__Session()

    def get_context(self):
        return self.__session

    def save_changes(self):
        self.__session.commit()

    def close(self):
        self.__Session.remove()
