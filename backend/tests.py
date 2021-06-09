"""Script to seed database."""

from unittest import TestCase
from server import app
import test_data_creation


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        test_data_creation.example_data_using_crud()


