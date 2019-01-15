import unittest
from api.models import User, Incident

class TestModels(unittest.TestCase):
    def setUp(self):
        self.redflags = {}
        self.users = []

    def test_create_User(self):
        # create user
        user = User(
            firstname="Benjamin",
            lastname="Mayanja",
            email="vibenjamin6@gmail.com",
            phone_number = "0819823089",
            username = 'v1b3m'
        )

        # return user
        print(user)

        # convert user to dictionary
        user.to_dictionary()

        # add user to list
        self.users.append(user)

    def test_create_Incident(self):
        # create an incident
        incident = Incident(
                            createdBy = 1,
                            type = 'red-flag',
                            location = {
                                "location": {
                                            "lat": "1.45",
                                            "long": "1.89"
                                            }
                                        },
                            status = "Pending",
                            comment = "I have no idea"
                            )

        # return an incident  
        print(incident)

        # Add incident to array
        self.redflags[incident.id] = incident