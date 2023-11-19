#!/usr/bin/python3
"""
base for all data types
"""
from uuid import uuid4
from datetime import datetime
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
base = declarative_base()


class Base():
    """
    The above class is a base class that provides default
    values for id, created_at, and updated_at attributes
    if no arguments are provided, and updates the object's
    attributes with the provided arguments if any.
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        The function initializes an object with default values for id,
        created_at, and updated_at if no arguments are provided,
        otherwise it updates the object's attributes with the provided
        arguments.
        """
        from mods import dbstorage
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'id' not in kwargs.keys():
                kwargs['id'] = str(uuid4())
            if 'created_at' not in kwargs.keys():
                kwargs['created_at'] = datetime.now()
            else:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' not in kwargs.keys():
                kwargs['updated_at'] = datetime.now()
            else:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')
            self.__dict__.update(kwargs)
        dbstorage.new(self)

    def save(self):
        """
        The function updates the "updated_at" attribute of an
        object with the current datetime.
        """
        from mods import dbstorage
        self.updated_at = datetime.now()
        dbstorage.new(self)
        dbstorage.save()

    def to_json(self, iso=False):
        """
        The function `to_json` converts an object's attributes
        into a dictionary and adds additional information such
        as the object's class name and the creation and update timestamps.
        """
        my_dict = {}
        my_dict.update(self.__dict__)
        my_dict.update({'__class__':
                        (str(type(self)).split('.')[-1]).split('\'')[0]})
        if iso is True:
            my_dict['created_at'] = self.created_at.isoformat()
            my_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict.keys():
            del my_dict['_sa_instance_state']
        return my_dict

    def delete(self):
        """
        The above function deletes the object that it is called on.
        """
        # storage deletion to be added
        del self

    def __str__(self):
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        my_dic = {}
        return '[{}] ({}) {}'.format(
            cls, self.id,
            self.to_json(iso=True))
