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
    if (not data or
        not isinstance(data, str)
        or data.isspace()):
        return False
    return True

def phone_number(data):
    """ This will check for a valid phone number """
    if re.match("((\(\d{3}\)?)|(\d{3}-))?\d{3}-\d{4}", data):
        return True
    return False

def missing_location_data(data):
    """ This will check if location data is missing from the request """
    if 'location' not in data:
        return "Location data not found"
    elif not string_data(data['location']):
        return "location must be a string"
    return None
        
def missing_comment_data(data):
    """ This will check if comment data is missing from the request """
    if 'comment' not in data:
        return "Comment data not found"
    elif not string_data(data['comment']):
        return "comment must be a string"
    return None

def wrong_status_data(data):
    """ This will verify status data """
    if 'status' not in data:
        return "Status data not found"
    elif not string_data(data['status']):
        return 'status must be a string'
    elif data['status'] not in ['​under investigation', 'rejected', 'resolved']:
        return "status can only be `​under investigation`,`rejected` or `resolved`"
    return None

def wrong_type_data(data):
    """ This will verify type data """
    if not string_data(data['type']):
        return "type must be a string"
    elif data['type'] not in ['red-flag', 'intervention']:
        return "types can only be `red-flag` or `intervention`"
    return None

def valid_create_data(data):
    """ This will verify data required to create an incident """
    if ('created_by' not in data or 'type' not in data or
                'comment' not in data or 'location' not in data):
        return "Some Information is missing from the request"
    elif validate_add_redflag_data(data):
        return validate_add_redflag_data(data)
    return None

def validate_add_redflag_data(data):
    """ This function will be used to
        validate input_data """
    try:
        if missing_location_data(data):
            raise TypeError(missing_location_data(data  ))
        if wrong_type_data(data):
            raise TypeError(wrong_type_data(data))
        if missing_comment_data(data):
            raise TypeError(missing_comment_data(data))
        if not isinstance(data['created_by'], int):
            raise TypeError("created_by must be an integer")
    except (TypeError, ValueError) as error:
        return str(error)
    return None
