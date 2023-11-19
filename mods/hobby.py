#!/usr/bin/python3
from mods.base import Base, base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Hobby(Base, base):
    __tablename__ = 'hobbies'
    name = Column(String(60), nullable=False)
    link = Column(String(120))
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    description = Column(String(1024))
