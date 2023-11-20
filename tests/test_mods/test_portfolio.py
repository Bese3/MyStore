# #!/usr/bin/python3
# """
# testing base class for all data
# """
# from mods.portifolio import Portfolio
# from datetime import datetime
# import unittest
# import time


# class TestUser(unittest.TestCase):
#     """
#     The `TestBase` class contains test methods to check the
#     documentation strings, initialization, and save functionality
#     of the `user` class in the `mods.user` module.
#     """
#     def setUp(self):
#         new_dict = {
#             'email': 'bese@gmail.com',
#             'password': '12345678'
#         }
#         self.user = User(**new_dict)
#     def test_docs(self):
#         """
#         The function `test_docs` checks that the documentation
#         strings for certain classes and methods in the `mods.user`
#         module are not empty.
#         """
#         self.assertNotEqual(__import__('mods').user.__doc__, "")
#         self.assertNotEqual(__import__('mods').user.User.__doc__, "")

#     def test_init(self):
#         """
#         The `test_init` function tests the initialization
#         and conversion to JSON of a `User` object.
#         """
#         a = self.user
#         self.assertTrue(type(a.id) is str)
#         self.assertTrue(type(a.created_at) is datetime)
#         self.assertTrue(type(a.updated_at) is datetime)
#         self.assertTrue(a.created_at < a.updated_at)

#         new_dict = a.to_json(iso=True)
#         new_dict['id'] = 'new_id'
#         b = User(**new_dict)
#         self.assertFalse(a is b)
#         self.assertTrue(a.created_at == b.created_at)
#         self.assertTrue(a.updated_at == b.updated_at)
#         self.assertTrue(b.created_at < b.updated_at)
#         a.save()
#         b.save()
#         a.delete()
#         b.delete()

#     def test_save(self):
#         """
#         The function tests whether the updated_at attribute of
#         an object changes after calling the save() method.
#         """
#         new_dict = {
#             'email': 'bese@gmail.com',
#             'password': '12345678'
#         }
#         a = User(**new_dict)
#         time_now = a.updated_at
#         time.sleep(1)
#         a.save()
#         self.assertFalse(time_now == a.updated_at)
#         a.delete()


#     def test_to_json(self):
#         """
#         The function `test_to_json` checks if the keys '__class__',
#         'created_at', 'updated_at', and 'id' are present in the
#         dictionary returned by the `to_json` method of the Base class.
#         """
#         a = self.user
#         new_dict = a.to_json()
#         self.assertTrue('__class__' in new_dict.keys())
#         self.assertTrue('created_at' in new_dict.keys())
#         self.assertTrue('updated_at' in new_dict.keys())
#         self.assertTrue('id' in new_dict.keys())
#         a.save()
#         a.delete()
