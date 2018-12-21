import unittest
from api import app
import json
from api.models import User, Incident

class TestRedflags(unittest.TestCase):
    def setUp(self):
        self.app_tester = app.test_client()
        self.redflags = []

    def test_get_all_redflags(self):
        # test when the list is empty 
        response = self.app_tester.get('/api/v1/red-flags')
        print(response)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'],200)

        #test when there's data in the list
        input_data = {
                    "status": "Approved", 
                    "location": {"lat": "0.96", "long": "1.23"}, 
                    "createdBy": "Benjamin", 
                    "type": "red-flag", 
                    "comment": "I am the greatest"
                    }
        self.app_tester.post('/api/v1/red-flags', json=input_data)
        response1 = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response1.data)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data), 2)

    def test_get_specific_redflag(self):
        response = self.app_tester.get('/api/v1/red-flags/1')
        print(response)# test when the list# test when the list is empty 
        response = self.app_tester.get('/api/v1/red-flags')
        print(response)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'],200) 
        response = self.app_tester.get('/api/v1/red-flags')
        print(response)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'],200)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(data['error']), 25)
        # self.assertEqual(data['error'],"The redflag doesn't exist")

        # test when the record exists
        input_data = {
                    "status": "Approved", 
                    "location": {"lat": "0.96", "long": "1.23"}, 
                    "createdBy": "Benjamin", 
                    "type": "red-flag", 
                    "comment": "I am the greatest"
                    }
        self.app_tester.post('/api/v1/red-flags', json=input_data)
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']

        response = self.app_tester.get('/api/v1/red-flags/{}'.format(id))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_add_redflag_record(self):
        input_data = {
                    "status": "Approved", 
                    "location": {"lat": "0.96", "long": "1.23"}, 
                    "createdBy": "Benjamin", 
                    "type": "red-flag", 
                    "comment": "I am the greatest"
                    }
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['message'],'Created red-flag record')
        self.assertEqual(data['status'], 201)
        
        # test when there is missing data
        input_data.clear()
        input_data = {
                    "status": "Approved", 
                    "location": {"lat": "0.96", "long": "1.23"}, 
                    "createdBy": "Benjamin", 
                    "type": "red-flag", 
                    }
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Some Information is missing from the request')

        # test when there is no data in request
        response = self.app_tester.post('/api/v1/red-flags')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 400)


    def test_delete_redflag(self):
        # test when record doesn't exist
        response = self.app_tester.delete('/api/v1/red-flags/2')
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['message']), 42)
        self.assertEqual(data['status'], 204)

        # test when the record exists
        input_data = {
                    "status": "Approved", 
                    "location": {"lat": "0.96", "long": "1.23"}, 
                    "createdBy": "Benjamin", 
                    "type": "red-flag", 
                    "comment": "I am the greatest"
                    }
        self.app_tester.post('/api/v1/red-flags', json=input_data)
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']

        response = self.app_tester.delete('/api/v1/red-flags/{}'.format(id))
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_patch_redflag_location(self):
        input_data = {"location": "2375812"}

        # test when record doesn't exist
        response = self.app_tester.patch('/api/v1/red-flags/1/location', 
                                        json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['message']), 74)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 
                        "Are you are magician? Cause the record just disappeared from our database."
                        )

        # test when there is no data in request
        response = self.app_tester.patch('/api/v1/red-flags/1/location')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 400)

        # test when the record exists
        input_data.clear()
        input_data = {
                    "status": "Approved", 
                    "location": {"lat": "0.96", "long": "1.23"}, 
                    "createdBy": "Benjamin", 
                    "type": "red-flag", 
                    "comment": "I am the greatest"
                    }
        self.app_tester.post('/api/v1/red-flags', json=input_data)
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']
        print(id)
        input_location = {"location": "fhkdd"}
        response = self.app_tester.patch('/api/v1/red-flags/{}/location'.format(id), json=input_location)
        data = json.loads(response.data)

        self.assertEqual(data['status'], 201)

    def test_patch_redflag_comment(self):
        input_data = {"comment": "I am sick"}

        # test when the record doesn't exist
        response = self.app_tester.patch('/api/v1/red-flags/1/comment', json=input_data)
        print(response)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['message']), 31)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'],"Sorry, the record doesn't exist")

        # test when there is no data in request
        response = self.app_tester.patch('/api/v1/red-flags/1/comment')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 400)

        # test when the record exists
        input_data.clear()
        input_data = {
                    "status": "Approved", 
                    "location": {"lat": "0.96", "long": "1.23"}, 
                    "createdBy": "Benjamin", 
                    "type": "red-flag", 
                    "comment": "I am the greatest"
                    }
        self.app_tester.post('/api/v1/red-flags', json=input_data)
        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data)
        id = data['data'][0]['id']
        print(id)
        input_location = {"comment": "fhkdd"}
        response = self.app_tester.patch('/api/v1/red-flags/{}/comment'.format(id), json=input_location)
        data = json.loads(response.data)

        self.assertEqual(data['status'], 204)

    def test_hello_world(self):
        response = self.app_tester.get('/')
        # data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Hello' in response.get_data(as_text=True))

