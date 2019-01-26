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
    
def string_or_integer_data(data):
    """ This will check for string or integer exists """
    if isinstance(data, int):
        return True
    elif string_data(data):
        return True
    return False

def string_data(data):
    """ This willcheck for string data """
    if (not isinstance(data, str)
        or data.isspace()):
        return False
    return True

def phone_number(data):
    """ This will check for a valid phone number """
    if re.match("((\(\d{3}\)?)|(\d{3}-))?\d{3}-\d{4}", data):
        return True
    return False
