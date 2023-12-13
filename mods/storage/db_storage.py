#!/usr/bin/python3
"""
common db storage for models
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
import MySQLdb
from os import getenv
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
    The `DBStorage` class is a Python class that provides methods
    for interacting with a MySQL database, including creating a new
    database, retrieving instances of a specified class, adding new objects,
    retrieving objects based on class name and ID, retrieving relations
    from the database, saving new objects, reloading the session object,
    deleting objects from the database, and closing the session.
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
                                  user="mystore_dev",
                                  passwd=str(getenv("mystore_pwd")),
                                  charset="utf8")
        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS mystore_dev_db")
        connect.commit()
        cursor.close()
        connect.close()
        self.__engine = create_engine('mysql+mysqldb://'
                                      '{}:{}@{}:3306/{}'.format('mystore_dev',
                                                                str(getenv("mystore_pwd")),
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
        The function "new" adds a new object to the session.
        """
        self.__session.add(obj)

    def get(self, cls, id):
        """
        The function returns an object based on the class name and
        its ID, or None if not found.
        """
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value
            if type(value) is Friend and value.user_id == id:
                return value
        return None

    def get_relation(self, cls, id, sub_class):
        """
        The function `get_relation` retrieves a relation from the
        database based on the provided class, id, and sub_class.
        """
        if cls not in classes.values():
            return None
        my_query = self.__session.query(cls).filter(eval("User." + sub_class)).filter(User.id == id).all()
        return my_query

    def save(self):
        """
        The save function is used to save a new object by
        committing changes to the session.
        """
        self.__session.commit()

    def reload(self):
        """
        The `reload` function creates all the necessary tables
        in the database and initializes a new session object.
        """
        base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()

    def delete(self, obj=None):
        """
        The function deletes an object from a database.
        """
        if obj is None:
            return
        self.__session.delete(obj)

    def close(self):
        """
        The close function closes the session and reloads it.
        """
        self.__session.close()
        self.reload()
