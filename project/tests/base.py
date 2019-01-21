from flask_testing import TestCase

from project.server import app
from db import DatabaseConnection

db_name = DatabaseConnection()

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        self.input_data = {"location": "0.96, 1.23",
                           "created_by": 1, "type": "red-flag",
                           "comment": "I am the greatest"
                           }
        db_name.create_incidents_table()

    def tearDown(self):
        db_name.delete_all_incidents()
