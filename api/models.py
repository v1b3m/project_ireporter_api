import random
from datetime import datetime
import uuid

class User:
    def __init__(self, firstname, lastname, othernames, 
                email, phone_number, username, registered, is_admin):
        self._id = int(uuid.uuid4())
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.registered = registered
        self.is_admin = is_admin

    def to_dict(self):
        return {
                'id': self._id, 'firstname': self.firstname, 
                'lastname': self.lastname, 'othername': self.othernames, 
                'email': self.email, 'phone_number': self.phone_number, 
                'username': self.phone_number, 'registered': self.registered, 
                'is_admin': self.is_admin
                }
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Incident:
    def __init__(self, created_by, _type, location, status, 
                comment, images=None, videos=None):
        self._id = random.randint(1, 9999999)
        self.createdOn = datetime.now()
        self.createdBy = created_by
        self.type = _type
        self.location = location
        self.status = status
        self.Images = images
        self.Videos = videos
        self.comment = comment

    def to_dict(self):
        return {
                'id': self._id, 'createdOn': self.createdOn, 
                'createdBy': self.createdBy, 'type': self.type, 
                'location': self.location, 'status': self.status, 
                'Images': self.Images, 'Videos': self.Videos, 
                'comment': self.comment
                }
    def __repr__(self):
        return '<Incident {}>'.format(self._id)


