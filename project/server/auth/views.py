from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt
from db import DatabaseConnection

auth_blueprint = Blueprint('auth', __name__)
from manage import db_name


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
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

# define the API resources
registration_view = RegisterAPI.as_view('register_api')


# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)