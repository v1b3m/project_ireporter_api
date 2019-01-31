# """ This script will test all the intervention api endpoints """
# import unittest
# import json
# from project.server import app
# from project.tests.base import BaseTestCase
# from project.tests.helpers import (login_user, register_user,
#                                    add_intervention)


# class TestEditIntervention(BaseTestCase):
#     """ This class will handle all the tests """    
#     def test_edit_intervention_status(self):
#         """ Test for editing status """
#         # log in user
#         register_user(self)
#         login_response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(login_response.data
#                                   )['data'][0]['token']
#                        )

#         input_data = {"status": "djhdjfj"}
#         response = self.client.patch('/api/v2/interventions/200/status',
#                                      content_type='application/json',
#                                      data=json.dumps(input_data),
#                                      headers=headers)

#         data = json.loads(response.data)

#         self.assertEqual(
#             data['error'], "You need to be an admin to access this route")
#         self.assertTrue(data['status'] == 403)

#     def test_edit_status_while_admin(self):
#         """ This will test editing status while user is admin """
#         # log in user
#         register_user(self)
#         login_response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(login_response.data
#                                   )['data'][0]['token']
#                        )

#         # obtain user id
#         user_id = json.loads(login_response.data)['data'][0]['user']['userid']

#         # make user an admin
#         self.db_name.make_admin(user_id)

#         # send request witn no data
#         response = self.client.patch(
#             '/api/v2/red-flags/200/status', headers=headers)
#         data = json.loads(response.data)
#         self.assertTrue(data['status'] == 400)

#     def test_update_status_with_wrong_data(self):
#         """ This test will attempt to edit status with wrong data """
#         # log in user
#         register_user(self)
#         login_response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(login_response.data
#                                   )['data'][0]['token']
#                        )

#         # obtain user id
#         user_id = json.loads(login_response.data)['data'][0]['user']['userid']

#         # make user an admin
#         self.db_name.make_admin(user_id)

#         # send request without status data
#         input_data = {"statu": "sjkj"}

#         # send request
#         response = self.client.patch('/api/v2/interventions/200/status',
#                                      content_type='application/json',
#                                      data=json.dumps(input_data),
#                                      headers=headers)
#         data = json.loads(response.data)
#         self.assertTrue(data["error"] == 'Status data not found')

#         # send request with integer status
#         input_data = {"status": 1}

#         # send request
#         response = self.client.patch('/api/v2/interventions/200/status',
#                                      content_type='application/json',
#                                      data=json.dumps(input_data),
#                                      headers=headers)
#         data = json.loads(response.data)
#         self.assertTrue(data["status"] == 400)

#     def test_edit_status_with_no_request_data(self):
#         """ This will test editing status while user is admin """
#         # log in user
#         register_user(self)
#         login_response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(login_response.data
#                                   )['data'][0]['token']
#                        )

#         # obtain user id
#         user_id = json.loads(login_response.data)['data'][0]['user']['userid']

#         # make user an admin
#         self.db_name.make_admin(user_id)

#         # send request witn no data
#         response = self.client.patch(
#             '/api/v2/interventions/200/status', headers=headers)
#         data = json.loads(response.data)
#         self.assertTrue(data['status'] == 400)

#     def test_edit_redflag_with_correct_data(self):
#         """ Test correct data to update status """
#         # log in user
#         register_user(self)
#         login_response = login_user(self)

#         # get token
#         headers = dict(Authorization='Bearer ' +
#                        json.loads(login_response.data
#                                   )['data'][0]['token']
#                        )

#         # obtain user id
#         user_id = json.loads(login_response.data)['data'][0]['user']['userid']

#         # make user an admin
#         self.db_name.make_admin(user_id)

#         # create intervention record
#         input_data = self.intervention_data
#         add_intervention(self, headers, input_data)

#         # get intervention record id
#         response = self.client.get('/api/v2/interventions', headers=headers)
#         data = json.loads(response.data)
#         intervention_id = data['data'][0]['incident_id']

#         # edit the red-flag status
#         # send request with wrong status format
#         input_data = {"status": "rejected"}
#         response = self.client.patch('/api/v2/interventions/%d/status' % intervention_id,
#                                      content_type='application/json',
#                                      data=json.dumps(input_data),
#                                      headers=headers)
#         data = json.loads(response.data)
#         self.assertTrue(data["status"] == 201)

#         # edit non-existent red-flag
#         response = self.client.patch('/api/v2/interventions/200/status',
#                                      content_type='application/json',
#                                      data=json.dumps(input_data),
#                                      headers=headers)
#         data = json.loads(response.data)
#         self.assertTrue(data["error"] == 404)
