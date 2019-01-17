""" This script will test the user and incident models """
import unittest
from api.models import User, Incident


class TestModels(unittest.TestCase):
    """ This class willc contain all the tests """

    def setUp(self):
        """ Set up all variables required for the tests """
        self.redflags = {}
        self.users = {}

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
        
        # add user to dictionary
        self.users[user.id] = user

        # convert user to dictionary
        user.to_dictionary()

    def return_user(self):
        """ this function will return users """
        return self.users.values()[0]
        
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
        self.redflags[incident.flag_id] = incident

    def return_an_incident(self):    
        """ This function will return an incident """
        red_flag = self.redflags.values()[0]
        self.assertIn('User', red_flag)

        
