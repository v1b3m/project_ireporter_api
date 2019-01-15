import unittest
from api import app
import json
from api.models import User, Incident
from helpers import input_data

class TestRedflags(unittest.TestCase):
    def setUp(self):
        self.app_tester = app.test_client()
        self.redflags = {}
        self.input_data = input_data

    def tearDown(self):
        self.redflags.clear()

    def test_get_all_redflags_when_dict_empty(self):
        """ Test for getting all red-flags when list is empty"""
        self.redflags.clear()
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['status'] == 200)

    def test_get_all_redflags_when_there_is_data(self):
        input_data = self.input_data
        self.app_tester.post('/api/v1/red-flags', json=input_data)
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)
        self.assertIsNotNone(data['data'][0])
        self.assertTrue(len(data) == 2)

    def test_get_specific_redflag_when_list_empty(self):
        """ Test for getting non-existent red-flag """
        response = self.app_tester.get('/api/v1/red-flags/1')
        data = json.loads(response.data)
        self.assertTrue(data['status'] == 404)
        self.assertIn("doesn't exist", data['error'])

    def test_get_specific_redflag_when_data_exists(self):
        """ Test for getting existent red-flags """
        # create a red-flag
        input_data = self.input_data
        self.app_tester.post('/api/v1/red-flags', json=input_data)

        # get the red-flag's id
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']

        # get the red-flag with the returned id
        response = self.app_tester.get('/api/v1/red-flags/{}'.format(id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["data"])
        self.assertFalse(data['data'][0]['type'] == 'intervention')

    def test_add_redflag_record(self):
        """ Test for adding a red-flag """
        input_data = self.input_data
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data['data']), 1)
        self.assertIn('Created red-flag', data['data'][0]['message'])
        self.assertFalse(data['status'] == 404)
        
    def test_add_redflag_record_when_request_has_missing_data(self):
        """ Test for adding a red-flag when the request has missing data """
        # create input_data with missing data
        input_data = {
            "status": "Approved", 
            "location": {"lat": "0.96", "long": "1.23"}, 
            "createdBy": "Benjamin" 
        }
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        data = json.loads(response.data)
        self.assertIn('Information is missing', data['error'])
        self.assertTrue(len(data) == 2)

    def test_add_redflag_when_request_has_no_data(self):
        """ Test for adding a red-flag when the request has no data """
        # post empty request
        response = self.app_tester.post('/api/v1/red-flags')
        data = json.loads(response.data)
        self.assertIn('Empty',data['error'])
        self.assertIsNot(response.status_code, 404)


    def test_delete_redflag_when_record_is_not_there(self):
        """ Test for deleting a non-existent red-flag """
        response = self.app_tester.delete('/api/v1/red-flags/2')
        data = json.loads(response.data)
        self.assertTrue(response.status_code == 200)
        self.assertIn("Oops",data['message'])
        self.assertEqual(data['status'], 204)

    def test_delete_redflag_when_record_exists(self):
        """ Test for deleting existent red-flag """
        # create red-flag
        input_data = self.input_data
        self.app_tester.post('/api/v1/red-flags', json=input_data)

        # get red-flag record id
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']

        # delete red-flag whose id has been returned
        response = self.app_tester.delete('/api/v1/red-flags/{}'.format(id))
        data = json.loads(response.data)
        self.assertIn('deleted',data['data'][0]['message'])

    def test_patch_redflag_location_when_record_is_not_existent(self):
        input_data = {"location": "2375812"}
        response = self.app_tester.patch('/api/v1/red-flags/1/location', 
                                        json=input_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['message']) == 74)
        self.assertEqual(data['error'], 400)
        self.assertIn("Are you are magician?", data['message'])

    def test_patch_redflag_when_request_has_no_data(self):
        # send empty patch request to server
        response = self.app_tester.patch('/api/v1/red-flags/1/location')
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Please provide a location')

    def test_patch_redflag_record_when_it_exists(self):
        # create red-flag record
        input_data = self.input_data
        self.app_tester.post('/api/v1/red-flags', json=input_data)

        # get red-flag record id
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']

        # patch red-flag whose id has been returned
        input_location = {"location": "fhkdd"}
        response = self.app_tester.patch('/api/v1/red-flags/{}/location'.format(id), json=input_location)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 201)
        self.assertIn("Updated", data['data'][0]['message'])

    def test_patch_redflag_comment_when_record_is_none_existent(self):
        input_data = {"comment": "I am sick"}
        response = self.app_tester.patch('/api/v1/red-flags/1/comment', json=input_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'] == "Sorry, the record doesn't exist")

    def test_patch_redflag_when_there_is_no_data_in_request(self):
        # send empty patch request to server
        response = self.app_tester.patch('/api/v1/red-flags/1/comment')
        data = json.loads(response.data)
        self.assertIn('provide a comment',data['error'])

    def test_patch_redflag_when_it_exists(self):
        # create red-flag record
        input_data = self.input_data
        self.app_tester.post('/api/v1/red-flags', json=input_data)

        # get red-flag record id
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']

        # patch red-flag record whose id has been returned
        input_location = {"comment": "fhkdd"}
        response = self.app_tester.patch('/api/v1/red-flags/{}/comment'.format(id), json=input_location)
        data = json.loads(response.data)

    def test_hello_world(self):
        """ Test for the index page """
        response = self.app_tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello', response.get_data(as_text=True))
