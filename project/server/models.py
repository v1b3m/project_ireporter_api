""" These models will be used to define the user
    and red-flag instances """
from datetime import datetime
import uuid


class User:
    """ This class is what will define any given user """

    def __init__(self, **kwargs):
        self.user_id = int(uuid.uuid4())
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.othernames = None
        self.email = kwargs['email']
        self.phone_number = kwargs['phone_number']
        self.username = kwargs['username']
        self.registered = datetime.now()
        self.is_admin = False

    def to_dictionary(self):
        """ this method will convert the user
            instance to a dictionary """
        return {
            'id': self.user_id, 'firstname': self.firstname,
            'lastname': self.lastname, 'othername': self.othernames,
            'email': self.email, 'phone_number': self.phone_number,
            'username': self.phone_number, 'registered': self.registered,
            'is_admin': self.is_admin
        }


class Incident:
    """ Both red-flag and intervention records will be
        created using this class """

    def __init__(self, **kwargs):
        self.flag_id = int(str(int(uuid.uuid4()))[:10])
        self.created_on = datetime.now()
        self.created_by = kwargs['created_by']
        self.type = kwargs['type']
        self.location = kwargs['location']
        self.status = "Pending"
        self.images = None
        self.videos = None
        self.comment = kwargs['comment']
