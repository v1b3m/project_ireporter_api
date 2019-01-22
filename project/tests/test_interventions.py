""" This script will test all the intervention api endpoints """
import unittest
import json
from project.server import app
from project.tests.base import BaseTestCase


class TestRedflags(BaseTestCase):
    """ This class will handle all the tests """

    def test_get_all_redflags_when_dict_empty(self):
        """ Test for getting all red-flags when list is empty"""
        response = self.client.get('/api/v1/interventions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['status'] == 404)