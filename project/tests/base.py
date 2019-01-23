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
        db_name.create_incidents_table()
        db_name.create_user_table()
        user_id = db_name.create_user(firstname='benjamin', lastname='mayanja',
                            othernames='', username='v1b3m', email='v122e@gmi.com',
                            password='1234', phone_number='2309908' )
        self.input_data = {"location": "0.96, 1.23",
                           "created_by": user_id, "type": "red-flag",
                           "comment": "I am the greatest"
                           }
        self.intervention_data = {"location": "0.96, 1.23",
                           "created_by": user_id, "type": "intervention",
                           "comment": "I am the greatest"
                           }

    def tearDown(self):
        db_name.delete_all_incidents()
        db_name.delete_all_users()