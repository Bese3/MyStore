#!/usr/bin/python3
"""
music class
"""
from mods.base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
base = declarative_base()


class Music(Base, base):
    """
    The class "Music" represents a table in a database with columns
    for name, link, and user_id.
    """
    __tablename__ = 'musics'
    name = Column(String(60), nullable=False)
    link = Column(String(120))
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
