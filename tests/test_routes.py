import unittest
from api import app
import json

class TestRedflags(unittest.TestCase):
    def setUp(self):
        self.app_tester = app.test_client()

    def test_get_all_redflags(self):
        response = self.app_tester.get('/api/v1/red-flags')
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data'][0]['createdBy'],'Benjamin')
        # self.assertEqual(data['data'][1]['id'], 2)

    def test_get_specific_redflag(self):
        response = self.app_tester.get('/api/v1/red-flags/1')
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 9)
        self.assertEqual(data['data']['type'],'red-flag')

        response = self.app_tester.get('/api/v1/red-flags/2000')
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(data['message']), 25)
        self.assertEqual(data['message'],"The redflag doesn't exist")



    def test_add_redflag_record(self):
        input_data = {"status": "Approved", "Videos": ["ben.mp4","love.avi"], 
            "location": {"lat": "0.96", "long": "1.23"}, "createdBy": "Benjamin", "Images": ["me.jpg"], 
            "createdOn": "2018-21-23, 21:15", "type": "red-flag", "id": 14, 
            "comment": "I am the greatest"}

        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['message'],'Created redflag record')
        self.assertEqual(data['status'], 201)

    def test_delete_redflag(self):
        response = self.app_tester.delete('/api/v1/red-flags/2')
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['status'], 204)
        self.assertEqual(data['data'][0]['id'],2)

    def test_patch_redflag_location(self):
        input_data = {
            "location": "2375812",
        }
        response = self.app_tester.patch('/api/v1/red-flags/1/location', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['status'], 204)
        self.assertEqual(data['data'][0]['message'],"Updated red-flag record's location")

    def test_patch_redflag_comment(self):
        input_data = {
            "comment": "I am sick",
        }
        response = self.app_tester.patch('/api/v1/red-flags/1/comment', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['status'], 204)
        self.assertEqual(data['data'][0]['message'],"Updated red-flag record's comment")
