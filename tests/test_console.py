import unittest
import os
from models import storage
from models.state import State
from models.place import Place
from console import HBNBCommand
from io import StringIO
import sys

class TestHBNBCommandCreate(unittest.TestCase):
    """Test the HBNBCommand create method"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        self.console.onecmd("create State name=\"California\"")
        self.console.onecmd("create Place city_id=\"0001\" user_id=\"0001\" name=\"My_little_house\" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297")

    def tearDown(self):
        """Tear down test environment"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_create_state(self):
        """Test creating a State with name"""
        output = StringIO()
        sys.stdout = output
        self.console.onecmd('create State name="California"')
        sys.stdout = sys.__stdout__
        state_id = output.getvalue().strip()
        self.assertIn(state_id, storage.all())

        state = storage.all()[f"State.{state_id}"]
        self.assertEqual(state.name, "California")

    def test_create_place(self):
        """Test creating a Place with various attributes"""
        output = StringIO()
        sys.stdout = output
        self.console.onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10

