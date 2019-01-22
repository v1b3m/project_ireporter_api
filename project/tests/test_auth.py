import unittest
import json
import time

from project.tests.base import BaseTestCase
from project.tests.helpers import register_user, login_user

from manage import db_name

class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        response = register_user(self)
        data = json.loads(response.data.decode())
        self.assertEqual(int(data['status']), 200)
        self.assertTrue(data['data'][0]['user'])
        self.assertTrue(data['data'][0]['token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_alredy_registered_user(self):
        """ Test registration with aready registered email """
        # create user
        db_name.create_user(firstname='Benjamin', lastname='Mayanja',
                            othernames='', username='v1b3m', email='test@test.com',
                            password='123456', phone_number='0703-755-919')
        with self.client:
            response = register_user(self)
        data = json.loads(response.data.decode())
        print(data['status'])
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'User already exists. Please Log in.'
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """ Test for login of registered user """
        with self.client:
            # user registration
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual(int(data['status']), 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # registered user login
            response = login_user(self, 'test@test.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self, 'test@test.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == "User does not exist.")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            response = register_user(self)
            data = json.loads(response.data)
            self.assertEqual(int(data['status']), 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # user login
            response = login_user(self, 'test@test.com', '123456')
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer '+json.loads(
                        response.data
                    )['data'][0]['token']
                )
            )
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # user registration
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual(int(data['status']), 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # user login
            response = login_user(self, 'test@test.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # invalid token logout
            time.sleep(11)
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer '+json.loads(
                        response.data.decode()
                    )['data'][0]['token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.'
            )
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual(int(data['status']), 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # user login
            response = login_user(self, 'test@test.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # blacklist a valid token
            db_name.blacklist_token(
                token=json.loads(response.data.decode())['data'][0]['token']
            )

            # blacklisted valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer '+json.loads(
                        response.data.decode()
                    )['data'][0]['token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)
