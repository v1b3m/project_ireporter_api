import unittest
from api.models import User, Incident

class TestModels(unittest.TestCase):
    def setUp(self):
        self.redflags = []
        self.users = []

    def test_create_User(self):
        user = User(
            firstname="Benjamin",
            lastname="Mayanja",
            email="vibenjamin6@gmail.com",
            phone_number = "0819823089",
            username = 'v1b3m'
        )
        print(user)
        user.to_dictionary()
        self.users.append(user)


    def test_create_Incident(self):
        incident = Incident(
                            createdBy = 1, 
                            _type = 'red-flag', 
                            location = {
                                "location": {
                                            "lat": "1.45",
                                            "long": "1.89"
                                            }
                                        }, 
                            status = "Pending", 
                            comment = "I have no idea"
                            )
        print(incident)
        self.redflags.append(incident)