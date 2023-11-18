#!/usr/bin/python3
"""
user class
"""
from mods.base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
base = declarative_base()


class User(Base, base):
    """
    The class "User" represents a user in a database with attributes
    such as email, password, first name, last name, contact,
    and a relationship to books.
    """
    __tablename__ = 'users'
    email = Column(String(60), nullable=False)
    password = Column(String(60), nullable=False)
    first_name = Column(String(60))
    last_name = Column(String(60))
    contact = Column(String(60))
    books = relationship('Books', backref='user',
                         cascade='all, delete')
    musics = relationship('Music', backref='user',
                          cascade='all, delete')
    movies = relationship('Movie', backref='user',
                          cascade='all, delete')
    portfolios = relationship('Portfolio', backref='user',
                          cascade='all, delete')
    friends = relationship('Friend', backref='user',
                          cascade='all, delete')
    hobbies = relationship('Hobby', backref='user',
                          cascade='all, delete')    
