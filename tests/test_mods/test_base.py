#!/usr/bin/python3
"""
testing base class for all data
"""
from mods.base import Base
from datetime import datetime
import unittest
import time



class TestBase(unittest.TestCase):
    """
    The `TestBase` class contains test methods to check the
    documentation strings, initialization, and save functionality
    of the `Base` class in the `mods.base` module.
    """
    def test_docs(self):
        """
        The function `test_docs` checks that the documentation
        strings for certain classes and methods in the `mods.base`
        module are not empty.
        """
        self.assertNotEqual(__import__('mods').base.__doc__, "")
        self.assertNotEqual(__import__('mods').base.Base.__doc__, "")
        self.assertNotEqual(__import__('mods').base.Base.__init__.__doc__, "")
        self.assertNotEqual(__import__('mods').base.Base.save.__doc__, "")
        self.assertNotEqual(__import__('mods').base.Base.to_json.__doc__, "")
        self.assertNotEqual(__import__('mods').base.Base.delete.__doc__, "")

    def test_init(self):
        """
        The `test_init` function tests the initialization
        and conversion to JSON of a `Base` object.
        """
        a = Base()
        self.assertTrue(type(a.id) is str)
        self.assertTrue(type(a.created_at) is datetime)
        self.assertTrue(type(a.updated_at) is datetime)
        self.assertTrue(a.created_at < a.updated_at)

        new_dict = a.to_json()
        b = Base(**new_dict)
        self.assertFalse(a is b)
        self.assertTrue(a.id is b.id)
        self.assertTrue(a.created_at == b.created_at)
        self.assertTrue(a.updated_at == b.updated_at)
        self.assertTrue(b.created_at < b.updated_at)
        del a
        del b

    def test_save(self):
        """
        The function tests whether the updated_at attribute of
        an object changes after calling the save() method.
        """
        a = Base()
        time_now = a.updated_at
        time.sleep(2)
        a.save()
        self.assertFalse(time_now == a.updated_at)
        del a

    def test_to_json(self):
        """
        The function `test_to_json` checks if the keys '__class__',
        'created_at', 'updated_at', and 'id' are present in the
        dictionary returned by the `to_json` method of the Base class.
        """
        a = Base()
        new_dict = a.to_json()
        self.assertTrue('__class__' in new_dict.keys())
        self.assertTrue('created_at' in new_dict.keys())
        self.assertTrue('updated_at' in new_dict.keys())
        self.assertTrue('id' in new_dict.keys())
        print(new_dict)
