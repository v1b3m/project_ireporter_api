""" This script will test all the intervention api endpoints """
import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.helpers import (login_user, register_user,
                                   add_intervention)

class TestRedflags(BaseTestCase):
    """ This class will handle all the tests """

    def test_get_all_intervention_when_dict_empty(self):
        """ Test for getting all interventions when list is empty"""
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        response = self.client.get('/api/v2/interventions', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['status'] == 404)
        self.assertTrue(data['error'] == "There are no interventions")

    def test_get_all_interventions_when_there_is_data(self):
        """ This will test for getting all stored interventions """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        input_data = self.intervention_data
        add_intervention(self, headers, input_data)
        response = self.client.get('/api/v2/interventions', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)
        self.assertIsNotNone(data['data'][0])
        self.assertTrue(len(data) == 2)
    

    def test_get_specific_intervention_when_list_empty(self):
        """ Test for getting non-existent intervention """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        response = self.client.get(
            '/api/v2/interventions/200000', headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data['status'] == 404)
        self.assertIn("doesn't exist", data['error'])

    def test_get_specific_redflag_when_data_exists(self):
        """ Test for getting existent red-flags """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        # create an intervention
        input_data = self.intervention_data
        add_intervention(self, headers, input_data)

        # get the intervention's id
        response = self.client.get('/api/v2/interventions', headers=headers)
        data = json.loads(response.data)
        intervention_id = data['data'][0]['incident_id']

        # get the intervention with the returned id
        response = self.client.get(
            '/api/v2/interventions/{}'.format(intervention_id), headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["data"])
        self.assertFalse(data['data'][0]['type'] == 'red-flag')

    def test_add_intervention_record(self):
        """ Test for adding a red-flag """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        input_data = self.intervention_data
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data['data']), 1)
        self.assertIn('Created intervention', data['data'][0]['message'])
        self.assertFalse(data['status'] == 404)

    def test_add_intervention_record_when_request_has_missing_data(self):
        """ Test for adding an intervention when the request has missing data """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        # create input_data with missing data
        input_data = {
            "location": {"lat": "0.96", "long": "1.23"},
            "created_by": "Benjamin"
        }
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('Information is missing', data['error'])
        self.assertTrue(len(data) == 2)

    def test_add_intervention_when_request_has_no_data(self):
        """ Test for adding an intervention when the request has no data """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        # post empty request
        response = self.client.post('/api/v2/interventions', headers=headers)
        data = json.loads(response.data)
        self.assertIn('Empty', data['error'])
        self.assertIsNot(response.status_code, 404)

    def test_add_intervention_with_wrong_data(self):
        """ Test for adding an intervention with
            wrong request data """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        # integer location
        input_data = {
            "location": 3,
            "created_by": 12, "type": "intervention",
            "comment": "I am the greatest"
        }
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('location must be', data['message'])
        self.assertTrue(len(data) == 2)

        # integer redflag type
        input_data = {
            "location": "0.12, 3.44",
            "created_by": 12, "type": 4,
            "comment": "I am the greatest"
        }
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('type must be', data['message'])
        self.assertTrue(len(data) == 2)

        # integer comment in request
        input_data = {
            "location": "0.12, 3.44",
            "created_by": 12, "type": "red-flag",
            "comment": 34
        }
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('comment must be', data['message'])
        self.assertTrue(len(data) == 2)

        # request containing created_by as a string
        input_data = {
            "location": "0.12, 3.44",
            "created_by": "me", "type": "red-flag",
            "comment": "This is a new comment"
        }
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('created_by must be', data['message'])
        self.assertTrue(len(data) == 2)

    def test_delete_intervention_when_record_is_not_there(self):
        """ Test for deleting a non-existent intervention """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        response = self.client.delete(
            '/api/v2/interventions/2', headers=headers)
        data = json.loads(response.data)
        self.assertTrue(response.status_code == 404)
        self.assertIn("Oops", data['message'])
        self.assertEqual(data['status'], 404)

    def test_delete_intervention_when_record_exists(self):
        """ Test for deleting existent red-flag """
        # log in user
        register_user(self)
        response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(response.data
                                  )['data'][0]['token']
                       )

        # create an intervention
        input_data = self.intervention_data
        add_intervention(self, headers, input_data)

        # get red-flag record id
        response = self.client.get('/api/v2/interventions', headers=headers)
        data = json.loads(response.data)
        intervention_id = data['data'][0]['incident_id']

        # delete red-flag whose id has been returned
        response = self.client.delete(
            '/api/v2/interventions/{}'.format(intervention_id), headers=headers)
        data = json.loads(response.data)
        self.assertIn('deleted', data['data'][0]['message'])

    def test_edit_intervention_status(self):
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
        response = self.client.patch('/api/v2/interventions/200/status',
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
        response = self.client.patch('/api/v2/interventions/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["error"] == 'Status data not found')

        # send request with integer status
        input_data = {"status": 1}

        # send request
        response = self.client.patch('/api/v2/interventions/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["error"] == 400)

    def test_edit_status_with_no_request_data(self):
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
            '/api/v2/interventions/200/status', headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data['status'] == 400)

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

        # create intervention record
        input_data = self.intervention_data
        add_intervention(self, headers, input_data)

        # get intervention record id
        response = self.client.get('/api/v2/interventions', headers=headers)
        data = json.loads(response.data)
        intervention_id = data['data'][0]['incident_id']

        # edit the red-flag status
        # send request with wrong status format
        input_data = {"status": "rejected"}
        response = self.client.patch('/api/v2/interventions/%d/status' % intervention_id,
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["status"] == 201)

        # edit non-existent red-flag
        response = self.client.patch('/api/v2/interventions/200/status',
                                     content_type='application/json',
                                     data=json.dumps(input_data),
                                     headers=headers)
        data = json.loads(response.data)
        self.assertTrue(data["error"] == 404)
