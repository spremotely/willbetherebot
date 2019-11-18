from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.context import Context
from data.models import Base


class AlchemyContext(Context):

    def __init__(self, connection_string):
        engine = create_engine(connection_string)
        Base.metadata.create_all(engine)
        self.__session = sessionmaker(bind=engine)()

    def get_context(self):
        return self.__session

    def save_changes(self):
        self.__session.commit()

    def close(self):
        self.__session.close()
