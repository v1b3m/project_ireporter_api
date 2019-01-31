# import unittest
# import json
# from project.server import app
# from project.tests.base import BaseTestCase
# from project.tests.helpers import (login_user, register_user,
#                                    add_redflag)


# class TestGetRedflags(BaseTestCase):
#     """ This class will handle all the scenarios of getting a red-flag """
#     def test_get_all_redflags_when_dict_empty(self):
#         """ Test for getting all red-flags when list is empty"""
#         # log in user
#         register_user(self)
#         response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(response.data
#                                   )['data'][0]['token']
#                        )

#         response = self.client.get('/api/v2/red-flags', headers=headers)
#         data = json.loads(response.data)
#         self.assertEqual(response.status_code, 404)
#         self.assertTrue(data['status'] == 404)

#     def test_get_all_redflags_when_there_is_data(self):
#         """ This will test for getting all stored red-flags """
#         # log in user
#         register_user(self)
#         response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(response.data
#                                   )['data'][0]['token']
#                        )

#         input_data = self.input_data
#         add_redflag(self, headers, input_data)
#         response = self.client.get('/api/v2/red-flags', headers=headers)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 200)
#         self.assertIsNotNone(data['data'][0])
#         self.assertTrue(len(data) == 2)

#     def test_get_specific_redflag_when_list_empty(self):
#         """ Test for getting non-existent red-flag """
#         # log in user
#         register_user(self)
#         login_response = login_user(self)

#         response = self.client.get(
#             '/api/v2/red-flags/200000',
#             headers=dict(
#                 Authorization='Bearer '+json.loads(
#                     login_response.data
#                 )['data'][0]['token']
#             )
#         )
#         data = json.loads(response.data)
#         self.assertTrue(data['status'] == 404)
#         self.assertIn("doesn't exist", data['error'])

#     def test_get_specific_redflag_when_data_exists(self):
#         """ Test for getting existent red-flags """
#         # log in user
#         register_user(self)
#         login_response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(login_response.data
#                                   )['data'][0]['token']
#                        )

#         # create a red-flag
#         input_data = self.input_data
#         add_redflag(self, headers, input_data)

#         # get the red-flag's id
#         response = self.client.get('/api/v2/red-flags', headers=headers)
#         data = json.loads(response.data)
#         flag_id = data['data'][0]['incident_id']

#         # get the red-flag with the returned id
#         response = self.client.get(
#             '/api/v2/red-flags/{}'.format(flag_id),
#             headers=dict(
#                 Authorization='Bearer '+json.loads(
#                     login_response.data
#                 )['data'][0]['token']
#             )
#         )
#         data = json.loads(response.data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(data["data"])
#         self.assertFalse(data['data'][0]['type'] == 'intervention')