from .database import Base
from sqlalchemy import Column, Integer, String


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    date = Column(String)
    time = Column(String)
    link = Column(String)


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Legislation(Base):
    __tablename__ = "legislation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_num = Column(String)
    type = Column(String)
    title = Column(String)
    result = Column(String)
    action_text = Column(String)
    mtg_date = Column(String)


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_num = Column(String)
    name = Column(String)
    vote = Column(String)
