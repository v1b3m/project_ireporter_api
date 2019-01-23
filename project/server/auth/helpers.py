import re
""" This script will contain all helper functions for authentication """

def validate_registration_input(data):
    try:
        if not isinstance(data.get('firstname'), str):
            raise TypeError("Firstname should be a string")
        if not isinstance(data.get('lastname'), str):
            raise TypeError("Lastname should be a string")
        if data.get('othernames'):
            if not isinstance(data.get('othernames'), str):
                raise TypeError("Othernames should be a string")
        if not isinstance(data.get('password'), str):
            if not isinstance(data.get('password'), int):
                raise TypeError("Password should be a string or an integer")
        if len(data.get('email')) < 7:
            raise ValueError("Email too short.")
        if not re.match("[^@]+@[^@]+\.[^@]+", data.get('email')):
            raise ValueError("This email is not valid.")
        if not re.match("((\(\d{3}\)?)|(\d{3}-))?\d{3}-\d{4}", data.get('phone_number')):
            raise ValueError("Phone Number is invalid")
    except (TypeError, ValueError) as e:
        return str(e)

def validate_login_input(data):
    try:
        if not re.match("[^@]+@[^@]+\.[^@]+", data.get('email')):
            raise ValueError("This email is not valid.")
        if not isinstance(data.get('password'), str):
            if not isinstance(data.get('password'), int):
                raise TypeError("Password should be a string or an integer")
    except (TypeError, ValueError) as e:
        return str(e)
        
