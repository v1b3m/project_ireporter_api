import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.helpers import (login_user, register_user,
                                   add_intervention)

class TestAddIntervention(BaseTestCase):
    """ This will test all scenarios of adding an intervention """
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
            "title": "intervention",
            "comment": "I am the greatest"
        }
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('location must be', data['error'])
        self.assertTrue(len(data) == 2)


        # integer comment in request
        input_data = {
            "location": "0.12, 3.44",
            "title": "red-flag",
            "comment": 34
        }
        response = add_intervention(self, headers, input_data)
        data = json.loads(response.data)
        self.assertIn('comment must be', data['error'])
        self.assertTrue(len(data) == 2)

    