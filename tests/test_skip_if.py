import os
import unittest
import MySQLdb
from models.state import State
from models import storage

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not using db storage")
class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.db = MySQLdb.connect(
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB'),
            host=os.getenv('HBNB_MYSQL_HOST')
        )
        self.cursor = self.db.cursor()

    def tearDown(self):
        """Tear down test environment"""
        self.db.close()

    def test_create_state(self):
        """Test creating a State"""
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        new_state = State(name="California")
        new_state.save()

        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchone()[0]

        self.assertEqual(new_count, initial_count + 1)

if __name__ == "__main__":
    unittest.main()
