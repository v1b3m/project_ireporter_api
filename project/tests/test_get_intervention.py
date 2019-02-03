import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.helpers import (login_user, register_user,
                                   add_intervention)

class TestGetIntervention(BaseTestCase):
    """ This will test all scenarios of getting an intervention """
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