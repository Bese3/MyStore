#!/usr/bin/python3
"""
books class
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from mods.base import Base, base


class Book(Base, base):
    """
    The class "Books" represents a table in a database with
    columns for name, author, user ID, special link, and description.
    """
    __tablename__ = 'books'
    name = Column(String(60), nullable=False)
    author = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    link = Column(String(120))
    description = Column(String(1024))
