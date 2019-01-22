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
