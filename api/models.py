import random
from datetime import datetime
import uuid

class User:
    def __init__(self, **kwargs):
        self._id = int(uuid.uuid4())
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.othernames = kwargs['othernames']
        self.email = kwargs['email']
        self.phone_number = kwargs['phone_number']
        self.username = kwargs['username']
        self.registered = kwargs['registered']
        self.is_admin = kwargs['is_admin']

    def to_dictionary(self):
        return {
                '_id': self._id, 'firstname': self.firstname, 
                'lastname': self.lastname, 'othername': self.othernames, 
                'email': self.email, 'phone_number': self.phone_number, 
                'username': self.phone_number, 'registered': self.registered, 
                'is_admin': self.is_admin
                }
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Incident:
    def __init__(self, **kwargs):
        self._id = random.randint(1, 9999999)
        self.createdOn = datetime.now()
        self.createdBy = kwargs['createdBy']
        self.type = kwargs['_type']
        self.location = kwargs['location']
        self.status = kwargs['status']
        self.Images = None
        self.Videos = None
        self.comment = kwargs['comment']

    
    def __repr__(self):
        return '<Incident {}>'.format(self._id)

    def __iter__(self):
        yield '_id', self._id
        yield 'createdOn', self.createdOn
        yield 'createdBy', self.createdBy
        yield 'type', self.type
        yield 'location', self.location
        yield 'status', self.status
        yield 'Images', self.Images
        yield 'Videos', self.Videos
        yield 'comment', self.comment
