import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.helpers import (login_user, register_user,
                                   add_intervention)

class TestDeleteIntervention(BaseTestCase):
    """ This will test all scenarios of deleting an intervention """
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