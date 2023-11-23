#!/usr/bin/python3
"""
db storage for models
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
# from os import getenv
import MySQLdb
from mods.book import Book
from mods.friend import Friend
from mods.hobby import Hobby
from mods.movie import Movie
from mods.music import Music
from mods.portifolio import Portfolio
from mods.user import User, base
classes = {
    'Book': Book,
    'Friend': Friend,
    'Hobby': Hobby,
    'Movie': Movie,
    'Music': Music,
    'Portfolio': Portfolio,
    'User': User
}


class DBStorage:
    """
    class starts here
    """
    __session = None
    __engine = None

    def __init__(self):
        """
        The above function initializes a connection to a MySQL
        database and creates a new database if it
        doesn't already exist.
        """
        connect = MySQLdb.connect(host="localhost", port=3306,
                                  user="mystore_dev", passwd="mystore_dev_pwd",
                                  charset="utf8")
        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS mystore_dev_db")
        connect.commit()
        cursor.close()
        connect.close()
        self.__engine = create_engine('mysql+mysqldb://'
                                      '{}:{}@{}:3306/{}'.format('mystore_dev',
                                                                'mystore_dev_pwd',
                                                                'localhost',
                                                                'mystore_dev_db'))

    def all(self, cls=None):
        """
        The function `all` retrieves all instances of a specified
        class from a database and returns them
        in a dictionary format.
        """
        my_dict = {}
        if cls:
            my_query = self.__session.query(cls).all()
            for i in my_query:
                my_dict[str(cls.__name__) + "." + i.id] = i
            return my_dict
        for key, value in classes.items():
            my_query = self.__session.query(value).all()
            for i in my_query:
                my_dict[str(key) + "." + i.id] = i
        return my_dict

    def new(self, obj):
        """
        adding new object
        """
        self.__session.add(obj)

    def save(self):
        """
        saving new object
        """
        self.__session.commit()

    def reload(self):
        """
        reloading session object
        """
        base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()

    def delete(self, obj=None):
        """
        deleting an object from database
        """
        if obj is None:
            return
        self.__session.delete(obj)

    def close(self):
        """
        closing session
        """
        self.__session.close()
        self.reload()
