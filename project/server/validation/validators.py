""" This script will have all the validation functions """
import re

def email_data(data):
    """ This function will validate an email address """
    if (
        len(data) > 7 and
        re.match("[^@]+@[^@]+\.[^@]+", data)
    ):
        return True
    return False

def string_data(data):
    """ This willcheck for string data """
    if (not data or
        not isinstance(data, str)
            or data.isspace()):
        return False
    return True

def number_data(data):
    if (not data or
        not isinstance(data, int)):
        return False
    return True

def phone_number(data):
    """ This will check for a valid phone number """
    if re.match("((\(\d{3}\)?)|(\d{3}-))?\d{3}-\d{4}", data):
        return True
    return False

def missing_data(data, type):
    """ This will check for missing data in a request """
    if type == 'comment':
        if 'comment' not in data:
            return "Comment data not found"
        elif not string_data(data['comment']):
            return "comment must be a string"
        return None
    if type == 'location':
        if 'location' not in data:
            return "Location data not found"
        elif not string_data(data['location']):
            return "location must be a string"
        return None

def wrong_status_data(data):
    """ This will verify status data """
    if 'status' not in data:
        return "Status data not found"
    elif not string_data(data['status']):
        return 'status must be a string'
    elif data['status'] not in ['under investigation', 'rejected', 'resolved']:
        return "status can only be `under investigation`,`rejected` or `resolved`"
    return None

def wrong_title_data(data):
    """ This will verify type data """
    if 'title' not in data:
        return "Title data not found"
    elif not string_data(data['title']):
        return "title must be a string"
    return None

def valid_create_data(data):
    """ This will verify data required to create an incident """
    if ('title' not in data or 'comment' not in data or 'location' not in data):
        return "Some Information is missing from the request"
    elif validate_add_redflag_data(data):
        return validate_add_redflag_data(data)
    return None

def validate_add_redflag_data(data):
    """ This function will be used to
        validate input_data """
    try:
        if missing_data(data, 'location'):
            raise TypeError(missing_data(data, 'location'))
        if wrong_title_data(data):
            raise TypeError(wrong_title_data(data))
        if missing_data(data, 'comment'):
            raise TypeError(missing_data(data, 'comment'))
    except (TypeError, ValueError) as error:
        return str(error)
    return None

def validate_registration_input(data):
    try:
        if 'firstname' not in data:
            raise KeyError("Firstname data not found")
        elif not string_data(data['firstname']):
            raise TypeError("Firstname should be a string")
        if 'lastname' not in data:
            raise KeyError("Lastname data not found")
        elif not string_data(data['lastname']):
            raise TypeError("Lastname should be a string")
        if data['othernames']:
            if not string_data(data['othernames']):
                raise TypeError("Othernames should be a string")
        if 'password' not in data:
            raise KeyError("Password data not found")
        elif not string_data(data['password']):
            raise TypeError("Password should be a string")
        if 'username' not in data:
            raise KeyError("Username data not found")
        elif not string_data(data['username']):
            raise TypeError("Username should be a string")
        if 'email' not in data:
            raise KeyError("Email data not found")
        elif not email_data(data['email']):
            raise ValueError("This email is not valid.")
        if 'phone_number' not in data:
            raise KeyError("Phone_number data not found")
        elif not phone_number(data['phone_number']):
            raise ValueError("Phone Number is invalid")
    except (TypeError, ValueError, KeyError) as e:
        return str(e)

def validate_login_input(data):
    try:
        if not email_data(data['email']):
            raise ValueError("This email is not valid.")
        if not string_data(data['password']):
            raise TypeError("Password should be a string")
    except (TypeError, ValueError) as e:
        return str(e)