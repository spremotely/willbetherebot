import datetime

from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    user_name = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_bot = Column(Boolean)
    state = relationship("State", uselist=False, back_populates="user")

    def __init__(
            self,
            user_id,
            user_name,
            first_name,
            last_name,
            is_bot=False):
        self.id = user_id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.is_bot = is_bot

    def __repr__(self):
        return f"<User({self.id}, {self.user_name}, {self.first_name}, {self.last_name}, {self.is_bot})>"

    def __eq__(self, other):
        return other.id == self.id \
            and other.user_name == self.user_name \
            and other.first_name == self.first_name \
            and other.last_name == self.last_name \
            and other.is_bot == self.is_bot


class Chat(Base):

    __tablename__ = "chat"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    type = Column(String(50))
    state = relationship("State", uselist=False, back_populates="chat")

    def __init__(self, chat_id, chat_type):
        self.id = chat_id
        self.type = chat_type

    def __repr__(self):
        return f"<Chat({self.id}, {self.type})>"

    def __eq__(self, other):
        return other.id == self.id and other.type == self.type


class ChatState(Base):

    __tablename__ = "state"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id'))
    chat = relationship("Chat", back_populates="state")
    user_id = Column(BigInteger, ForeignKey('user.id'))
    user = relationship("User", back_populates="state")
    message_id = Column(BigInteger)
    entity_id = Column(BigInteger, ForeignKey('entity.id'))
    entity = relationship("Entity", back_populates="state")
    command = Column(String(50))
    state = Column(String(50))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, chat_id, user_id, message_id, command, state, entity_id=None):
        self.chat_id = chat_id
        self.user_id = user_id
        self.message_id = message_id
        self.command = command
        self.state = state
        self.entity_id = entity_id

    def __repr__(self):
        return f"<State({self.id}, {self.chat_id}, {self.user_id}, {self.message_id}, {self.command}, {self.state}, {self.updated_at})>"

    def __eq__(self, other):
        return other.id == self.id and \
            other.chat == self.chat and \
            other.user == self.user and \
            other.message_id == self.message_id and \
            other.entity == self.entity and \
            other.command == self.command and \
            other.state == self.state and \
            other.updated_at == self.updated_at


class Entity(Base):

    __tablename__ = "entity"

    id = Column(BigInteger, primary_key=True)
    entity_id = Column(Integer)
    entity_type = Column(String(50))
    state = relationship("State", uselist=False, back_populates="entity")

    def __init__(self, entity_id, entity_type):
        self.entity_id = entity_id
        self.entity_type = entity_type

    def __repr__(self):
        return f"<Entity({self.id}, {self.entity_id}, {self.entity_type})>"

    def __eq__(self, other):
        return other.id == self.id and \
            other.entity_id == self.entity_id and \
            other.entity_type == self.entity_type and \
            other.state == self.state


class Photo(Base):

    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    uri = Column(String(1000))
    location = relationship("Location", uselist=False, back_populates="photo")

    def __init__(self, uri):
        self.uri = uri

    def __repr__(self):
        return f"<Photo({self.id}, {self.uri}, {self.location})>"

    def __eq__(self, other):
        return other.id == self.id and other.uri == self.uri and other.location == self.location


class Location(Base):

    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    photo_id = Column(Integer, ForeignKey('photo.id'))
    photo = relationship("Photo", back_populates="location")
    longitude = Column(String(50))
    latitude = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return f"<Location({self.id}, {self.photo_id}, {self.longitude}, {self.latitude}, {self.created_at})>"

    def __eq__(self, other):
        return other.id == self.id and \
            other.photo_id == self.photo_id and \
            other.photo == self.photo and \
            other.longitude == self.longitude and \
            other.latitude == self.latitude and \
            other.created_at == self.created_at
