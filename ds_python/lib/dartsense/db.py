import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class PlayerAlias(Base):
    __tablename__ = 'player_alias'
    id = Column(Integer, primary_key=True)
    alias = Column(String(100))
