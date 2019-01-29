from flask_testing import TestCase

from project.server import app
from db import DatabaseConnection


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        self.db_name = DatabaseConnection()

        user_id = self.db_name.create_user(firstname='benjamin', lastname='mayanja',
                                           othernames='', username='v1b3m', email='tes1t@test.com',
                                           password='1234456', phone_number='2309908')
        self.input_data = {"location": "0.96, 1.23",
                           "created_by": user_id, "type": "red-flag",
                           "comment": "I am the greatest"
                           }
        self.intervention_data = {"location": "0.96, 1.23",
                                  "created_by": user_id, "type": "intervention",
                                  "comment": "I am the greatest"
                                  }

    def tearDown(self):
        self.db_name.delete_from_table('incidents')
        self.db_name.delete_from_table('users')
        self.db_name.delete_from_table('blacklist')
