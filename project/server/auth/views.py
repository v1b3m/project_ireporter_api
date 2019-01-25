from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, app
from project.server.auth.helpers import (token_required, generate_auth_token,
                validate_registration_input, validate_login_input)
from db import DatabaseConnection

auth_blueprint = Blueprint('auth', __name__)
db_name = DatabaseConnection()


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()

        # validate data
        if validate_registration_input(post_data):
            response_object = {
                "status": 400,
                "error": validate_registration_input(post_data)
            }
            return make_response(jsonify(response_object)), 400

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
                auth_token = generate_auth_token(user_id)
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
        # get the post data
        post_data = request.get_json()

        # validate data
        if validate_login_input(post_data):
            response_object = {
                "status": 400,
                "error": validate_login_input(post_data)
            }
            return make_response(jsonify(response_object)), 400

        try:
            # fetch the user data
            user = db_name.check_user(email=post_data.get('email'))
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
    @token_required
    def post(self):
        # mark the token as blacklisted
        auth_token = request.headers.get('Authorization').split(" ")[1]
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
