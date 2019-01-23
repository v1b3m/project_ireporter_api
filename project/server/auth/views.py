from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, app
from db import DatabaseConnection

from project.server.auth.helpers import (validate_registration_input,
                                    validate_login_input)

auth_blueprint = Blueprint('auth', __name__)
db_name = DatabaseConnection()
import jwt
class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):

        # check for empty request
        if not request.is_json:
            return jsonify({
                'error': 'Request Cannot Be Empty',
                'status': 400
            }), 400

        # get the post data
        post_data = request.get_json()

        # check for missing data in request
        if ('firstname' not in post_data or 'lastname' not in post_data or
            'username' not in post_data or 'othernames' not in post_data or
            'email' not in post_data or 'password' not in post_data or
            'phone_number' not in post_data or 'othernames' not in post_data):
            return jsonify({
                'status': 400,
                'error': 'Some Information is missing from the request'
            }), 400

        # validate the input data
        if validate_registration_input(post_data):
            return jsonify({"error":400,
                            "message": validate_registration_input(post_data)
                            }), 400

        # check if user already exists
        user = db_name.check_user(email=post_data.get('email'))
        if not user:
            try:
                user_id = db_name.create_user(firstname=post_data.get('firstname'),
                    lastname=post_data.get('lastname'), othernames=post_data.get('othernames'),
                    username=post_data.get('username'), email=post_data.get('email'),
                    password=post_data.get('password'), phone_number=post_data.get('phone_number'))
                user = db_name.check_user(email=post_data.get('email'))
                # generate auth token
                auth_token = db_name.generate_auth_token(user_id)
                responseObject = {
                    'status': '200',
                    'data': [{
                        'token': auth_token.decode(),
                        "user": user
                    }] 
                }
                return make_response(jsonify(responseObject)), 201
            except:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.'
            }
            return make_response(jsonify(responseObject)), 202

class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):

        # check for empty request
        if not request.is_json:
            return jsonify({
                'error': 'Request Cannot Be Empty',
                'status': 400
            }), 400

        # get the post data
        post_data = request.get_json()

        # check for missing data in request
        if ( 'email' not in post_data or 'password' not in post_data):
            return jsonify({
                'status': 400,
                'error': 'Some Information is missing from the request'
            }), 400

        # validate the input data
        if validate_login_input(post_data):
            return jsonify({"error":400,
                            "message": validate_login_input(post_data)
                            }), 400

        try:
            # fetch the user data
            user = db_name.check_user(email=post_data.get('email'))
            if user and bcrypt.check_password_hash(
                user['password'], post_data.get('password')
            ):
                auth_token = db_name.generate_auth_token(user['userid'])
                if auth_token:
                    responseObject = {
                        'status': 200,
                        'data': [{
                            "token": auth_token.decode(),
                            "user": user
                        }]
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except:
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500

class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                
                try:
                    db_name.blacklist_token(auth_token)
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
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

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')


# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)