""" This script will test all the intervention api endpoints """
import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase


class TestRedflags(BaseTestCase):
    """ This class will handle all the tests """

    def test_get_all_intervention_when_dict_empty(self):
        """ Test for getting all interventions when list is empty"""
        response = self.client.get('/api/v1/interventions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['status'] == 404)
    
    def test_get_all_interventions_when_there_is_data(self):
        """ This will test for getting all stored interventions """
        input_data = self.intervention_data
        self.client.post('/api/v1/interventions', json=input_data)
        response = self.client.get('/api/v1/interventions')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)
        self.assertIsNotNone(data['data'][0])
        self.assertTrue(len(data) == 2)

    def test_get_specific_intervention_when_list_empty(self):
        """ Test for getting non-existent intervention """
        response = self.client.get('/api/v1/interventions/200000')
        data = json.loads(response.data)
        self.assertTrue(data['status'] == 404)
        self.assertIn("doesn't exist", data['error'])

    def test_get_specific_redflag_when_data_exists(self):
        """ Test for getting existent red-flags """
        # create an intervention
        input_data = self.intervention_data
        self.client.post('/api/v1/interventions', json=input_data)

        # get the intervention's id
        response = self.client.get('/api/v1/interventions')
        data = json.loads(response.data)
        intervention_id = data['data'][0]['incident_id']

        # get the intervention with the returned id
        response = self.client.get('/api/v1/interventions/{}'.format(intervention_id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["data"])
        self.assertFalse(data['data'][0]['type'] == 'red-flag')
    
    def test_add_intervention_record(self):
        """ Test for adding a red-flag """
        input_data = self.intervention_data
        response = self.client.post('/api/v1/interventions', json=input_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data['data']), 1)
        self.assertIn('Created intervention', data['data'][0]['message'])
        self.assertFalse(data['status'] == 404)

    def test_add_intervention_record_when_request_has_missing_data(self):
        """ Test for adding an intervention when the request has missing data """
        # create input_data with missing data
        input_data = {
            "location": {"lat": "0.96", "long": "1.23"},
            "created_by": "Benjamin"
        }
        response = self.client.post('/api/v1/interventions', json=input_data)
        data = json.loads(response.data)
        self.assertIn('Information is missing', data['error'])
        self.assertTrue(len(data) == 2)

    def test_add_intervention_when_request_has_no_data(self):
        """ Test for adding an intervention when the request has no data """
        # post empty request
        response = self.client.post('/api/v1/interventions')
        data = json.loads(response.data)
        self.assertIn('Empty', data['error'])
        self.assertIsNot(response.status_code, 404)

    def test_add_intervention_with_wrong_data(self):
        """ Test for adding an intervention with
            wrong request data """
        # integer location
        input_data = {
            "location": 3,
            "created_by": 12, "type": "intervention",
            "comment": "I am the greatest"
        }
        response = self.client.post('/api/v1/interventions', json=input_data)
        data = json.loads(response.data)
        self.assertIn('location must be', data['message'])
        self.assertTrue(len(data) == 2)

        # integer redflag type
        input_data = {
            "location": "0.12, 3.44",
            "created_by": 12, "type": 4,
            "comment": "I am the greatest"
        }
        response = self.client.post('/api/v1/interventions', json=input_data)
        data = json.loads(response.data)
        self.assertIn('type must be', data['message'])
        self.assertTrue(len(data) == 2)

        # integer comment in request
        input_data = {
            "location": "0.12, 3.44",
            "created_by": 12, "type": "red-flag",
            "comment": 34
        }
        response = self.client.post('/api/v1/interventions', json=input_data)
        data = json.loads(response.data)
        self.assertIn('comment must be', data['message'])
        self.assertTrue(len(data) == 2)

        # request containing created_by as a string
        input_data = {
            "location": "0.12, 3.44",
            "created_by": "me", "type": "red-flag",
            "comment": "This is a new comment"
        }
        response = self.client.post('/api/v1/interventions', json=input_data)
        data = json.loads(response.data)
        self.assertIn('created_by must be', data['message'])
        self.assertTrue(len(data) == 2)