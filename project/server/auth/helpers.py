""" This script will contain all helper functions for authentication """
import re
import jwt
import datetime
from db import DatabaseConnection
from project.server import app
from functools import wraps
from flask import request, make_response, jsonify
from project.server.validation.validators import (string_data, 
    string_or_integer_data, email_data, phone_number)

db_name = DatabaseConnection()

def validate_registration_input(data):
    try:
        if not string_data(data['firstname']):
            raise TypeError("Firstname should be a string")
        if not string_data(data['lastname']):
            raise TypeError("Lastname should be a string")
        if data['othernames']:
            if not string_data(data['othernames']):
                raise TypeError("Othernames should be a string")
        if not string_data(data['password']):
            raise TypeError("Password should be a string")
        if not string_or_integer_data(data['username']):   
            raise TypeError("Username should be a string or an integer")
        if not email_data(data['email']):
            raise ValueError("This email is not valid.")
        if not phone_number(data['phone_number']):
            raise ValueError("Phone Number is invalid")
    except (TypeError, ValueError) as e:
        return str(e)


def validate_login_input(data):
    try:
        if not email_data(data['email']):
            raise ValueError("This email is not valid.")
        if not string_data(data['password']): 
            raise TypeError("Password should be a string")
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
                    'status': 401,
                    'error': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 401,
                'error': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
    return decorated_function


def admin_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                if db_name.is_admin(resp):
                    return func(*args, **kwargs)
                else:
                    responseObject = {
                        'status': 403,
                        'error': "You need to be an admin to access this route"
                    }
                    return make_response(jsonify(responseObject)), 403
            else:
                responseObject = {
                    'status': 401,
                    'error': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 401,
                'error': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
    return decorate


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
