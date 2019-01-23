import re, jwt, datetime
from db import DatabaseConnection
from project.server import app
from functools import wraps
from flask import request, make_response, jsonify
""" This script will contain all helper functions for authentication """

db_name = DatabaseConnection()

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

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        is_blacklisted = db_name.check_blacklist(auth_token)
        if is_blacklisted:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return func(*args, **kwargs)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
    return decorated_function

def generate_auth_token(user_id):
        """
        Generates the auth token string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
