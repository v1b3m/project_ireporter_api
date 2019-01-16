""" This script will test the user and incident models """
import unittest
from api.models import User, Incident


class TestModels(unittest.TestCase):
    """ This class willc contain all the tests """

    def setUp(self):
        """ Set up all variables required for the tests """
        self.redflags = {}
        self.users = []

    def test_create_user(self):
        """ This test will emulate user creation """
        # create user
        user = User(
            firstname="Benjamin",
            lastname="Mayanja",
            email="vibenjamin6@gmail.com",
            phone_number="0819823089",
            username='v1b3m'
        )

        # return user
        print(user)

        # convert user to dictionary
        user.to_dictionary()

        # add user to list
        self.users.append(user)

    def test_create_incident(self):
        """ This test will emulate creation of an incident """
        # create an incident
        incident = Incident(
            created_by=1,
            type='red-flag',
            location={
                "location": {
                    "lat": "1.45",
                    "long": "1.89"
                }
            },
            status="Pending",
            comment="I have no idea"
        )

        # return an incident
        print(incident)

        # Add incident to array
        self.redflags[incident.flag_id] = incident
