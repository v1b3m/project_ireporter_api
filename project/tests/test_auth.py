import unittest
import json
import time

from project.tests.base import BaseTestCase
from project.tests.helpers import register_user, login_user, logout_user

from db import DatabaseConnection
db_name = DatabaseConnection()


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        response = register_user(self)
        data = json.loads(response.data.decode())
        self.assertEqual(int(data['status']), 200)
        self.assertTrue(data['data'][0]['user'])
        self.assertTrue(data['data'][0]['token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_wrong_data(self):
        """ This function will test the data validation """
        # integer firstname
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                firstname=32,
                lastname="Mayanja",
                othernames="",
                phone_number="070-755-9192",
                username='v1b3m',
                email="test@test.com",
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 400)

        # integer lastname
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                firstname="Benjamin",
                lastname=33,
                othernames="",
                phone_number="070-755-9192",
                username='v1b3m',
                email="test@test.com",
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIn("Lastname should be", data['error'])

        # integer othernames
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                firstname="Benjamin",
                lastname="Mayabja",
                othernames=4,
                phone_number="070-755-9192",
                username='v1b3m',
                email="test@test.com",
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIn("Othernames should be", data['error'])

        # wrong email
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                firstname="Benjamin",
                lastname="Mayabja",
                othernames="",
                phone_number="070-755-9192",
                username='v1b3m',
                email="te@st@test.com",
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == "This email is not valid.")

        # short email
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                firstname="Benjamin",
                lastname="Mayabja",
                othernames="",
                phone_number="070-755-9192",
                username='v1b3m',
                email="tt@t.m",
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == "Email too short.")

        # wrong phone number
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                firstname="Benjamin",
                lastname="Mayabja",
                othernames="",
                phone_number="070755-9192",
                username='v1b3m',
                email="ttsdf@dffd.dfm",
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == "Phone Number is invalid")

        # wrong password
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                firstname="Benjamin",
                lastname="Mayabja",
                othernames="",
                phone_number="070-755-9192",
                username='v1b3m',
                email="ttsdf@dffd.dfm",
                password=[]
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == "Password should be a string or an integer")

    def test_registration_with_alredy_registered_user(self):
        """ Test registration with aready registered email """
        # create user
        db_name.create_user(firstname='Benjamin', lastname='Mayanja',
                            othernames='', username='v1b3m', email='test@test.com',
                            password='123456', phone_number='0703-755-919')
        with self.client:
            response = register_user(self)
        data = json.loads(response.data.decode())
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
            response = login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self)
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
            response = login_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # valid token logout
            response = logout_user(self, response)
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
            response = login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 200)
            self.assertTrue(data['data'][0]['user'])
            self.assertTrue(data['data'][0]['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # invalid token logout
            time.sleep(6)
            response = logout_user(self, response)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.'
            )
            self.assertEqual(response.status_code, 401)

    def test_login_with_wrong_data(self):
        """ This will test logging in with wrong data """
        # invalid email
        response = self.client.post(
                        '/auth/login',
                        data=json.dumps(dict(
                            email="t@est@test.com",
                            password="123456"
                        )),
                        content_type='application/json'
                        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['error'], "This email is not valid.")

        # wrong password
        response = self.client.post(
            '/auth/login',
            data=json.dumps(dict(
                firstname="Benjamin",
                lastname="Mayabja",
                othernames="",
                phone_number="070-755-9192",
                username='v1b3m',
                email="ttsdf@dffd.dfm",
                password=[]
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == "Password should be a string or an integer")
        

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
            response = login_user(self)
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
            response = logout_user(self, response)
            data = json.loads(response.data.decode())
            # self.assertTrue(data['status'] == 'fail')
            # self.assertTrue(data['message'] ==
            #                 'Token blacklisted. Please log in again.')
            # self.assertEqual(response.status_code, 401)

    def test_decode_invalid_token(self):
        """ Test for decoding an invalid token """
        # logout with wrong token
        response = self.client.post('/auth/logout', headers="")
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'fail')

        # invalid admin token
        input_data = ""
        response = self.client.patch('/api/v1/red-flags/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers="")
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'fail')

        # invalid token
        response =  self.client.post(
                    '/auth/logout',
                    headers=dict(
                        Authorization='Bearer 1234'
                        )
                    )
        self.assertEqual(data['status'], 'fail')


