#!/usr/bin/python3
"""
friend class
"""
from mods.base import Base, base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from mods.user import User


class Friend(Base, base):
    """
    The `Friend` class represents a relationship between
    users and their friends in a database table.
    """
    __tablename__ = 'friends'
    id = Column(String(60))
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False, primary_key=True)
    friend_id = Column(String(60), nullable=False,
                       primary_key=True)
    # strorage querying for friend id needed

    def friend_valid(self):
        from mods import dbstorage
        all_users_id = [i.id for i in dbstorage.all(User).values()]
        if self.friend_id == self.user_id:
            raise ValueError('friend cant be your self')
        if self.friend_id not in all_users_id:
            raise ValueError('friend is not found in the users category')
