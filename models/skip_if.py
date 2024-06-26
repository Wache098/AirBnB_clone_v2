import unittest
from models import storage

@unittest.skipIf(storage.type != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    def test_something(self):
