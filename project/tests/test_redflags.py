""" This script will test all the api endpoints """
import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.helpers import (login_user, register_user,
                get_flags, add_redflag)


class TestRedflags(BaseTestCase):
    """ This class will handle all the tests """

    def test_get_all_redflags_when_dict_empty(self):
        """ Test for getting all red-flags when list is empty"""
        # log in user
        register_user(self)
        response = login_user(self)

        response = get_flags(self, response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['status'] == 404)

    def test_get_all_redflags_when_there_is_data(self):
        """ This will test for getting all stored red-flags """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(response.data
                    )['data'][0]['token']
                )

        input_data = self.input_data
        add_redflag(self, headers, input_data)
        response = get_flags(self, response)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)
        self.assertIsNotNone(data['data'][0])
        self.assertTrue(len(data) == 2)

    def test_get_specific_redflag_when_list_empty(self):
        """ Test for getting non-existent red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        response = self.client.get(
            '/api/v1/red-flags/200000',
            headers=dict(
                    Authorization='Bearer '+json.loads(
                        login_response.data
                    )['data'][0]['token']
                )
            )
        data = json.loads(response.data)
        self.assertTrue(data['status'] == 404)
        self.assertIn("doesn't exist", data['error'])

    def test_get_specific_redflag_when_data_exists(self):
        """ Test for getting existent red-flags """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )
        
        # create a red-flag
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get the red-flag's id
        response = get_flags(self, login_response)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # get the red-flag with the returned id
        response = self.client.get(
            '/api/v1/red-flags/{}'.format(flag_id),
            headers=dict(
                    Authorization='Bearer '+json.loads(
                        login_response.data
                    )['data'][0]['token']
                )
            )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["data"])
        self.assertFalse(data['data'][0]['type'] == 'intervention')

    def test_add_redflag_record(self):
        """ Test for adding a red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        input_data = self.input_data
        response = add_redflag(self, headers, input_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data['data']), 1)
        self.assertIn('Created red-flag', data['data'][0]['message'])
        self.assertFalse(data['status'] == 404)

    def test_add_redflag_record_when_request_has_missing_data(self):
        """ Test for adding a red-flag when the request has missing data """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # create input_data with missing data
        input_data = {
            "location": {"lat": "0.96", "long": "1.23"},
            "created_by": "Benjamin"
        }
        response = add_redflag(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('Information is missing', data['error'])
        self.assertTrue(len(data) == 2)

    def test_add_redflag_when_request_has_no_data(self):
        """ Test for adding a red-flag when the request has no data """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )
        
        # post empty request
        response = self.client.post(
            '/api/v1/red-flags',
            headers=headers
            )
        data = json.loads(response.data)
        self.assertIn('Empty', data['error'])
        self.assertIsNot(response.status_code, 404)

    def test_add_redflag_with_integer_wrong_data(self):
        """ Test for adding a red-flag with
            wrong request data """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # integer location
        input_data = {
            "location": 3,
            "created_by": 12, "type": "red-flag",
            "comment": "I am the greatest"
        }
        response = add_redflag(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('location must be', data['message'])
        self.assertTrue(len(data) == 2)

        # integer redflag type
        input_data = {
            "location": "0.12, 3.44",
            "created_by": 12, "type": 4,
            "comment": "I am the greatest"
        }
        response = add_redflag(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('type must be', data['message'])
        self.assertTrue(len(data) == 2)

        # integer comment in request
        input_data = {
            "location": "0.12, 3.44",
            "created_by": 12, "type": "red-flag",
            "comment": 34
        }
        response = add_redflag(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('comment must be', data['message'])
        self.assertTrue(len(data) == 2)

        # request containing created_by as a string
        input_data = {
            "location": "0.12, 3.44",
            "created_by": "me", "type": "red-flag",
            "comment": "This is a new comment"
        }
        response = add_redflag(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('created_by must be', data['message'])
        self.assertTrue(len(data) == 2)

    def test_delete_redflag_when_record_is_not_there(self):
        """ Test for deleting a non-existent red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        response = self.client.delete('/api/v1/red-flags/2', headers=headers)
        data = json.loads(response.data)
        self.assertTrue(response.status_code == 200)
        self.assertIn("Oops", data['message'])
        self.assertEqual(data['status'], 204)

    def test_delete_redflag_when_record_exists(self):
        """ Test for deleting existent red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # create red-flag
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record id
        response = get_flags(self, login_response)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # delete red-flag whose id has been returned
        response = self.client.delete(
            '/api/v1/red-flags/{}'.format(flag_id),
            headers=headers)
        data = json.loads(response.data)
        self.assertIn('deleted', data['data'][0]['message'])

    def test_patch_redflag_location_when_record_is_not_existent(self):
        """ This will test patching a non existent red-flag's location """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        input_data = {"location": "2375812"}
        response = self.client.patch('/api/v1/red-flags/1/location',
                                        content_type='application/json',
                                        data=json.dumps(input_data),
                                        headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['message']) == 41)
        self.assertEqual(data['error'], 400)
        self.assertIn("doesn't exist", data['message'])

    def test_patch_redflag_when_request_has_no_data(self):
        """ This will test patching a red-flag when
            the request has no data """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # send empty patch request to server
        response = self.client.patch('/api/v1/red-flags/1/location', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Please provide a location')

    def test_patch_redflag_record_when_it_exists(self):
        """ Here we'll test patching an existent red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record flag_id
        response = get_flags(self,login_response)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag whose id has been returned
        input_data = {"location": "fhkdd"}
        response = self.client.patch('/api/v1/red-flags/{}/location'.format(flag_id),
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
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record flag_id
        response = get_flags(self, login_response)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag whose id has been returned
        input_data = {"location": 21}
        response = self.client.patch('/api/v1/red-flags/{}/location'.format(flag_id),
                                    content_type='application/json',
                                    data=json.dumps(input_data),
                                    headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn("location must be", data['message'])

        # patch red-flag without location data in request
        input_data = {"locatio": "0.12, 3.22"}
        response = self.client.patch('/api/v1/red-flags/{}/location'.format(flag_id),
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
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        input_data = {"comment": "I am sick"}
        response = self.client.patch(
            '/api/v1/red-flags/1/comment',
            content_type='application/json',
            data=json.dumps(input_data),
            headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'] ==
                        "Sorry, the red-flag record doesn't exist.")

    def test_patch_redflag_when_there_is_no_data_in_request(self):
        """ This will test patching a red-flag with an
            empty request """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # send empty patch request to server
        response = self.client.patch('/api/v1/red-flags/1/comment', headers=headers)
        data = json.loads(response.data)
        self.assertIn('provide a comment', data['error'])

    def test_patch_redflag_when_it_exists(self):
        """ This will test patching a red-flag that exists """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record id
        response = get_flags(self, login_response)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag record whose id has been returned
        input_data = {"comment": "fhkdd"}
        response = self.client.patch('/api/v1/red-flags/{}/comment'.format(flag_id),
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
        headers=dict(Authorization='Bearer '+
                    json.loads(login_response.data
                    )['data'][0]['token']
                )

        # create red-flag record
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record flag_id
        response = get_flags(self, login_response)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # patch red-flag with an integer comment
        input_data = {"comment": 21}
        response = self.client.patch('/api/v1/red-flags/{}/comment'.format(flag_id),
                                    content_type='application/json',
                                    data=json.dumps(input_data),
                                    headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn("comment must be", data['message'])

        # patch red-flag without comment data
        input_data = {"sdfjdk": "This is a new comment"}
        response = self.client.patch('/api/v1/red-flags/{}/comment'.format(flag_id),
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
