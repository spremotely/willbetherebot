import datetime

from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    user_name = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_bot = Column(Boolean)
    state = relationship("ChatState", uselist=False, back_populates="user")

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


class Chat(Base):

    __tablename__ = "chat"

    id = Column(BigInteger, primary_key=True)
    type = Column(String(50))
    state = relationship("ChatState", uselist=False, back_populates="chat")

    def __init__(self, chat_id, chat_type):
        self.id = chat_id
        self.type = chat_type

    def __repr__(self):
        return f"<Chat({self.id}, {self.type})>"



class ChatState(Base):

    __tablename__ = "chat_state"

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

    def __init__(self, chat, user, message_id, command, state, entity=None):
        self.chat = chat
        self.user = user
        self.message_id = message_id
        self.command = command
        self.state = state
        self.entity = entity

    def __repr__(self):
        return f"<State({self.id}, {self.chat}, {self.user}, {self.message_id}, {self.command}, {self.state}, {self.entity}, {self.updated_at})>"


class Entity(Base):

    __tablename__ = "entity"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    entity_id = Column(Integer)
    entity_type = Column(String(50))
    state = relationship("ChatState", uselist=False, back_populates="entity")

    def __init__(self, entity_id, entity_type):
        self.entity_id = entity_id
        self.entity_type = entity_type

    def __repr__(self):
        return f"<Entity({self.id}, {self.entity_id}, {self.entity_type})>"


class Photo(Base):

    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    uri = Column(String(1000))
    location = relationship("Location", uselist=False, back_populates="photo")

    def __init__(self, uri):
        self.uri = uri

    def __repr__(self):
        return f"<Photo({self.id}, {self.uri}, {self.location})>"


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
