#!/usr/bin/python3
"""
The code is importing the `DBStorage`class from the
`db_storage` module in the `mods.storage` package.
It then creates an instance of the `DBStorage`
class called `dbstorage` and calls the `reload()` method on it.
"""
from mods.storage.db_storage import DBStorage
dbstorage = DBStorage()
dbstorage.reload()
