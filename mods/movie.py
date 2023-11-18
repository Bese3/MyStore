#!/usr/bin/python3
"""
movie class
"""
from mods.base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
base = declarative_base()


class Movie(Base, base):
    """
    The class "Movie" represents a table in a database with
    columns for name, link, and description.
    """
    __tablename__ = 'movies'
    name = Column(String(60), nullable=False)
    link = Column(String(120))
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    description = Column(String(1024))
