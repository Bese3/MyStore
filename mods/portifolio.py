#!/usr/bin/python3
"""
Portfolio class
"""
from mods.base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
base = declarative_base()


class Portfolio(Base, base):
    """
    The class "Portfolio" represents a portfolio object with
    attributes such as name, link, user_id
    """
    __tablename__ = 'portfolios'
    name = Column(String(60), nullable=False)
    link = Column(String(120))
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    description = Column(String(1024))
