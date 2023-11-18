#!/usr/bin/python3
from mods.base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
base = declarative_base()


class Books(Base, base):
    __tablename__ = 'books'
    