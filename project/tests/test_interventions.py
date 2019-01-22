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

    def test_get_specific_intervention_when_list_empty(self):
        """ Test for getting non-existent intervention """
        response = self.client.get('/api/v1/interventions/200000')
        data = json.loads(response.data)
        self.assertTrue(data['status'] == 404)
        self.assertIn("doesn't exist", data['error'])