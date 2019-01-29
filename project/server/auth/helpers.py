""" This script will contain all helper functions for authentication """
import re
import jwt
import datetime
from db import DatabaseConnection
from project.server import app
from functools import wraps
from flask import request, make_response, jsonify

db_name = DatabaseConnection()

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

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        is_blacklisted = db_name.check_item('token', auth_token)
        if is_blacklisted:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def extract_token():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    return auth_token

def token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_token = extract_token()
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
        auth_token = extract_token()
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
