import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.helpers import (login_user, register_user,
                                   add_redflag)


class TestDeleteRedflags(BaseTestCase):
    """ This class will handle all the scenarios of deleting a red-flag """
    def test_delete_redflag_when_record_is_not_there(self):
        """ Test for deleting a non-existent red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        response = self.client.delete('/api/v2/red-flags/2', headers=headers)
        data = json.loads(response.data)
        self.assertTrue(response.status_code == 404)
        self.assertIn("Oops", data['message'])
        self.assertEqual(data['status'], 404)

    def test_delete_redflag_when_record_exists(self):
        """ Test for deleting existent red-flag """
        # log in user
        register_user(self)
        login_response = login_user(self)

        # get token
        headers = dict(Authorization='Bearer ' +
                       json.loads(login_response.data
                                  )['data'][0]['token']
                       )

        # create red-flag
        input_data = self.input_data
        add_redflag(self, headers, input_data)

        # get red-flag record id
        response = self.client.get('/api/v2/red-flags', headers=headers)
        data = json.loads(response.data)
        flag_id = data['data'][0]['incident_id']

        # delete red-flag whose id has been returned
        response = self.client.delete(
            '/api/v2/red-flags/{}'.format(flag_id),
            headers=headers)
        data = json.loads(response.data)
        self.assertIn('deleted', data['data'][0]['message'])