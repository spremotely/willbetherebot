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
    state = relationship("state", uselist=False, back_populates="user")


class Chat(Base):

    __tablename__ = "chat"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    type = Column(String(50))
    state = relationship("state", uselist=False, back_populates="chat")


class State(Base):

    __tablename__ = "state"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id'))
    char = relationship("chat", back_populates="state")
    user_id = Column(BigInteger, ForeignKey('user.id'))
    user = relationship("user", back_populates="state")
    message_id = Column(BigInteger)
    entity_id = Column(BigInteger, ForeignKey('entity.id'))
    entity = relationship("entity", back_populates="state")
    command = Column(String(50))
    state = Column(String(50))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Entity(Base):

    __tablename__ = "entity"

    id = Column(BigInteger, primary_key=True)
    entity_id = Column(Integer)
    entity_type = Column(String(50))
    state = relationship("state", uselist=False, back_populates="entity")


class Photo(Base):

    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    uri = Column(String(1000))
    location = relationship("location", uselist=False, back_populates="photo")


class Location(Base):

    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    photo_id = Column(Integer, ForeignKey('photo.id'))
    photo = relationship("photo", back_populates="location")
    Longitude = Column(String(50))
    Latitude = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
