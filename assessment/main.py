import unittest
from unittest import TestCase

import pytest
import requests
import json
import logging

## Global variables and functions
from pytest import fail


class XharkTankAssessment(TestCase):

    HEADERS = None

    def __init__(self, *args, **kwargs):

        unittest.TestCase.__init__(self, *args, **kwargs)
        self.HEADERS = {"Content-Type": "application/json"} # "X-Firebase-Auth": "INTERNAL_IMPERSONATE_USER_" + str(user),
        self.localhost = 'http://localhost:8081/'

        self.FIRST_PITCH_ID = ''

        self.POSITIVE_STATUS_CODES = [200, 201, 202, 203]
        self.NEGATIVE_STATUS_CODES = [400, 401, 402, 403, 404, 405, 409]

    ### Helper functions
    def get_api(self, endpoint):
      
        response = requests.get(self.localhost + endpoint, headers=self.HEADERS)
        self.print_curl_request_and_response(response)
        return response

    def post_api(self, endpoint, body):
       
        response = requests.post(self.localhost + endpoint, headers=self.HEADERS, data=body)
        self.print_curl_request_and_response(response)
        return response

    def print_curl_request_and_response(self, response):
    
        if(response.status_code in self.POSITIVE_STATUS_CODES):
         
            self.decode_and_load_json(response)

    def patch_api(self, endpoint, body):
       
        response = requests.patch(self.localhost + endpoint, headers = self.HEADERS, data = body)
        self.print_curl_request_and_response(response)
        return response

    def decode_and_load_json(self, response):
        try:
            text_response = response.content.decode('utf-8')
            data = json.loads(text_response)
        except Exception as e:
          
            logging.exception(str(e))
            return response
        return data
    ### Helper functions end here


    @pytest.mark.run(order=1)
    def test_0_get_on_empty_db_test(self):
        """When run with empty database, get calls should return success, and response should be an empty list """
        # print("test_get_on_empty_db_test")
        endpoint = 'pitch/'
        response_with_slash = self.get_api(endpoint)
        self.assertEqual(response_with_slash.status_code, 200)
        # print(self.decode_and_load_json(response_with_slash))
        response_length = len(self.decode_and_load_json(response_with_slash))
        # print("length of the response received = {}".format(response_length))
        self.assertEqual(response_length, 0)

    # First Post
    @pytest.mark.run(order=2)
    def test_1_post_first_pitch(self):
        """Post first Pitch and verify that it returns id in the response"""
        endpoint = 'pitch/'
        body = {
            "pitcherName": "Yakshit",
"pitchTitle": "Crio.Do - A Project Building Platform",
"pitchDetails" : "Learn Like You Would At India's Top Tech Companies. Work-experience based learning programs for developers Build professional projects like the top 1% developers. Master the latest full stack and backend tech with real work-ex. Crack developer jobs at the best tech companies.",
"expectedAmount" : 1000000000,
"equity": 25
        }
        response = self.post_api(endpoint, json.dumps(body))
        # print("verify that response status code is one of " + str(self.POSITIVE_STATUS_CODES))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        print('First post data: ', data)
        self.FIRST_PITCH_ID = data['id']
        # print('Assigned successfully' + str(self.FIRST_POST_ID))

    @pytest.mark.run(order=3)
    def test_2_get_single_pitch(self):  # Score 6
        """Post a new Pitch capture its Id, and verify its GET /pitch/{id} returns correct PITCH"""
        endpoint = 'pitch/'
        body = {
            "pitcherName": "Yakshit",
"pitchTitle": "Crio.Do - A Project Building Platform",
"pitchDetails" : "Learn Like You Would At India's Top Tech Companies. Work-experience based learning programs for developers Build professional projects like the top 1% developers. Master the latest full stack and backend tech with real work-ex. Crack developer jobs at the best tech companies.",
"expectedAmount" : 1000000000,
"equity": 25
        }

        response = self.post_api(endpoint, json.dumps(body))
        # print("verify that response status code is one of " + str(self.POSITIVE_STATUS_CODES))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        # print('First post data: ', data)

        # inserted, now get it using get api.
        endpoint = 'pitch/{}'.format(data["id"])
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        print('get single: ', data)
        self.assertEqual(data['pitcherName'], "Yakshit")
        self.assertEqual(data['pitchTitle'], "Crio.Do - A Project Building Platform")
        self.assertEqual(data['pitchDetails'], "Learn Like You Would At India's Top Tech Companies. Work-experience based learning programs for developers Build professional projects like the top 1% developers. Master the latest full stack and backend tech with real work-ex. Crack developer jobs at the best tech companies.")
        self.assertEqual(data['expectedAmount'], 1000000000)
        self.assertEqual(data['equity'], 25)



    @pytest.mark.run(order=4)
    def test_3_get_single_pitch_non_existent_test(self):
        """Try to access PITCH with some random id, and verify that it returns 404"""
        endpoint = 'pitch/0909'
        response = self.get_api(endpoint)
        # print('Status code for non existent meme: ', response.status_code)
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.run(order=5)
    def test_4_post_duplicate_pitch(self):
        """Verify that posting duplicate pitch return 409"""
        endpoint = 'pitch/'
        body = {
            "pitcherName": "Yakshit",
"pitchTitle": "Crio.Do - A Project Building Platform",
"pitchDetails" : "Learn Like You Would At India’s Top Tech Companies. Work-experience based learning programs for developers Build professional projects like the top 1% developers. Master the latest full stack and backend tech with real work-ex. Crack developer jobs at the best tech companies.",
"expectedAmount" : 1000000000,
"equity": 25
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.run(order=6)
    def test_5_post_empty_pitch(self):
        """Verify that API doesnt accept empty data in POST call"""
        endpoint = 'pitch/'
        body = {}
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)



if __name__ == '__main__':
    unittest.main()


