""" This script will test all the api endpoints """
import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.helpers import (login_user, register_user,
                                   add_redflag)


class TestRedflags(BaseTestCase):
    """ This class will handle all the tests """
    

    def test_patch_redflag_location_when_record_is_not_existent(self):
        """ This will test patching a non existent red-flag's location """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        input_data = {"location": "2375812"}
        response = self.client.patch('/api/v2/red-flags/1/location',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(len(data['message']) == 41)
        self.assertEqual(data['error'], 404)
        self.assertIn("doesn't exist", data['message'])

    def test_patch_redflag_when_request_has_no_data(self):
        """ This will test patching a red-flag when
            the request has no data """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # send empty patch request to server
        response = self.client.patch(
            '/api/v2/red-flags/1/location', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Request Cannot Be Empty')

    def test_patch_redflag_record_when_it_exists(self):
        """ Here we'll test patching an existent red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record flag_id
        response = self.client.get('/api/v2/red-flags', headers=headers)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag whose id has been returned
        input_data = {"location": "fhkdd"}
        response = self.client.patch('/api/v2/red-flags/{}/location'.format(flag_id),
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 201)
        self.assertIn("Updated", data['data'][0]['message'])

    def test_patch_redflag_with_wrong_location_data(self):
        """ Test for patching a redflag location with
            an integer location """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record flag_id
        response = self.client.get('/api/v2/red-flags', headers=headers)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag whose id has been returned
        input_data = {"location": 21}
        response = self.client.patch('/api/v2/red-flags/{}/location'.format(flag_id),
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn("location must be", data['error'])

        # patch red-flag without location data in request
        input_data = {"locatio": "0.12, 3.22"}
        response = self.client.patch('/api/v2/red-flags/{}/location'.format(flag_id),
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn("Location data", data['error'])

    def test_patch_redflag_comment_when_record_is_non_existent(self):
        """ This will test patching a non existent red-flag comment """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        input_data = {"comment": "I am sick"}
        response = self.client.patch(
            '/api/v2/red-flags/1/comment',
            content_type='application/json',
            data=json.dumps(input_data),
            headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'] ==
                        "Sorry, the red-flag record doesn't exist.")

    def test_patch_redflag_when_there_is_no_data_in_request(self):
        """ This will test patching a red-flag with an
            empty request """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # send empty patch request to server
        response = self.client.patch(
            '/api/v2/red-flags/1/comment', headers=headers)
        data = json.loads(response.data)
        self.assertIn('provide a comment', data['error'])

    def test_patch_redflag_when_it_exists(self):
        """ This will test patching a red-flag that exists """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record id
        response = self.client.get('/api/v2/red-flags', headers=headers)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag record whose id has been returned
        input_data = {"comment": "fhkdd"}
        response = self.client.patch('/api/v2/red-flags/{}/comment'.format(flag_id),
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)

    def test_patch_redflag_with_wrong_comment_data(self):
        """ Test for patching a redflag location with
            an integer comment """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record flag_id
        response = self.client.get('/api/v2/red-flags', headers=headers)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag with an integer comment
        input_data = {"comment": 21}
        response = self.client.patch('/api/v2/red-flags/{}/comment'.format(flag_id),
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn("comment must be", data['error'])

        # patch red-flag without comment data
        input_data = {"sdfjdk": "This is a new comment"}
        response = self.client.patch('/api/v2/red-flags/{}/comment'.format(flag_id),
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn("Comment data", data['error'])

    def test_hello_world(self):
        """ Test for the index page """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello', response.get_data(as_text=True))

    def test_edit_flag_status(self):
        """ Test for editing status """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        input_data = {"status": "djhdjfj"}
        response = self.client.patch('/api/v2/red-flags/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)

        data = json.loads(response.data)

        self.assertEqual(
            data['error'], "You need to be an admin to access this route")
        self.assertTrue(data['status'] == 403)

    def test_edit_status_while_admin(self):
        """ This will test editing status while user is admin """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # obtain user id
        user_id = json.loads(login_response.data)['data'][0]['user']['userid']

        # make user an admin
        self.db_name.make_admin(user_id)

        # send request witn no data
        response = self.client.patch(
            '/api/v2/red-flags/200/status', headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data['status'] == 400)

    def test_update_status_with_wrong_data(self):
        """ This test will attempt to edit status with wrong data """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # obtain user id
        user_id = json.loads(login_response.data)['data'][0]['user']['userid']

        # make user an admin
        self.db_name.make_admin(user_id)

        # send request without status data
        input_data = {"statu": "sjkj"}

        # send request
        response = self.client.patch('/api/v2/red-flags/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertEqual(data["error"], 'Status data not found')

        # send request with integer status
        input_data = {"status": 1}

        # send request
        response = self.client.patch('/api/v2/red-flags/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["status"] == 400)

        # send request with wrong status format
        input_data = {"status": "hey"}
        response = self.client.patch('/api/v2/red-flags/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["status"] == 400)

    def test_edit_redflag_with_correct_data(self):
        """ Test correct data to update status """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # obtain user id
        user_id = json.loads(login_response.data)['data'][0]['user']['userid']

        # make user an admin
        self.db_name.make_admin(user_id)

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record id
        response = self.client.get('/api/v2/red-flags', headers=headers)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # edit the red-flag status
        # send request with wrong status format
        input_data = {"status": "rejected"}
        response = self.client.patch('/api/v2/red-flags/%d/status' % flag_id,
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["status"] == 201)

        # edit non-existent red-flag
        response = self.client.patch('/api/v2/red-flags/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["error"] == 404)
