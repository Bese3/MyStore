#!/usr/bin/python3
"""
friend class
"""
from mods.base import Base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
base = declarative_base()


class Friend(Base, base):
    """
    The `Friend` class represents a relationship between
    users and their friends in a database table.
    """
    __tablename__ = 'friends'
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    friend_id = Column(String(60), nullable=False)
    # strorage querying for friend id needed
