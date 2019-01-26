from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, app
from project.server.auth.helpers import (token_required, 
            generate_auth_token, validate_registration_input,
            validate_login_input)
from db import DatabaseConnection
from flasgger import swag_from

auth_blueprint = Blueprint('auth', __name__)
db_name = DatabaseConnection()


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    @swag_from('../docs/register.yml')
    def post(self):
        # get the post data
        post_data = request.get_json()

        # check for missing data
        if (not post_data['firstname'] or not post_data['lastname'] or
            not post_data['password'] or not post_data['username'] or
            not post_data['email'] or not post_data['phone_number']):
            response_object = {
                "status": 400,
                "error": "Some information is missing. Try again"
            }
            return make_response(jsonify(response_object)), 400

        # validate data
        if validate_registration_input(post_data):
            response_object = {
                "status": 400,
                "error": validate_registration_input(post_data)
            }
            return make_response(jsonify(response_object)), 400

        # check if user already exists
        user = db_name.check_item('user',post_data['email'])
        if not user:
            try:
                user_id = db_name.create_user(firstname=post_data.get('firstname'),
                                              lastname=post_data.get('lastname'), othernames=post_data.get('othernames'),
                                              username=post_data.get('username'), email=post_data.get('email'),
                                              password=post_data.get('password'), phone_number=post_data.get('phone_number'))
                user = db_name.check_item('user', post_data['email'])
                # generate auth token
                auth_token = generate_auth_token(user_id)
                responseObject = {
                    'status': 201,
                    'data': [{
                        'token': auth_token.decode(),
                        "user": user
                    }]
                }
                return make_response(jsonify(responseObject)), 201
            except:
                responseObject = {
                    'status': 401,
                    'error': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 202,
                'error': 'User already exists. Please Log in.'
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    """
    User Login Resource
    """
    @swag_from('../docs/login.yml')
    def post(self):
        # get the post data
        post_data = request.get_json()

        # check for missing data
        if (not post_data['email'] or not post_data['password']):
            response_object = {
                "status": 400,
                "error": "Email or password missing. Try again!"
            }
            return make_response(jsonify(response_object)), 400

        # validate data
        if validate_login_input(post_data):
            response_object = {
                "status": 400,
                "error": validate_login_input(post_data)
            }
            return make_response(jsonify(response_object)), 400

        try:
            # fetch the user data
            user = db_name.check_item('user', post_data['email'])
            if user and bcrypt.check_password_hash(
                user['password'], post_data.get('password')
            ):
                auth_token = generate_auth_token(user['userid'])
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
                    'status': 404,
                    'error': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except:
            responseObject = {
                'status': 500,
                'error': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    @token_required
    @swag_from('../docs/logout.yml')
    def post(self):
        # mark the token as blacklisted
        auth_token = request.headers.get('Authorization').split(" ")[1]
        try:
            db_name.blacklist_token(auth_token)
            responseObject = {
                'status': 200,
                'message': 'Successfully logged out.'
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 400,
                'message': e
            }
            return make_response(jsonify(responseObject)), 400


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
