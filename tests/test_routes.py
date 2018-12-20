import unittest
from api import app
import json
from api.models import User, Incident

class TestRedflags(unittest.TestCase):
    def setUp(self):
        self.app_tester = app.test_client()
        self.redflags = []

    def test_get_all_redflags(self):
        response = self.app_tester.get('/api/v1/red-flags')
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data'][0]['createdBy'],'Benjamin')


    def test_get_specific_redflag(self):
        response = self.app_tester.get('/api/v1/red-flags/1')
        print(response)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['message']), 25)
        self.assertEqual(data['message'],"The redflag doesn't exist")



    def test_add_redflag_record(self):
        input_data = {"status": "Approved", 
            "location": {"lat": "0.96", "long": "1.23"}, "createdBy": "Benjamin",
             "type": "red-flag", "comment": "I am the greatest"}

        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['message'],'Created red-flag record')
        self.assertEqual(data['status'], 200)

    def test_delete_redflag(self):
        response = self.app_tester.delete('/api/v1/red-flags/2')
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['message']), 42)
        self.assertEqual(data['status'], 204)


    def test_patch_redflag_location(self):
        input_data = {
            "location": "2375812",
        }
        response = self.app_tester.patch('/api/v1/red-flags/1/location', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['message']), 74)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'],"Are you are magician? Cause the record just disappeared from our database.")

    def test_patch_redflag_comment(self):
        input_data = {
            "comment": "I am sick",
        }
        response = self.app_tester.patch('/api/v1/red-flags/1/comment', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['message']), 31)
        self.assertEqual(data['Status'], 400)
        self.assertEqual(data['message'],"Sorry, the record doesn't exist")
