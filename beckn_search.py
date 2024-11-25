import requests
from datetime import datetime
import uuid
from helper import Helper
class BecknSearch:
    def __init__(self, helper):
        self.helper = helper

    def generate_search_request(self, pickup, drop, catalogs, optimization_parameter):
        # Generate the search request using the Helper class
        return self.helper.generate_search_request(pickup, drop, catalogs, optimization_parameter)

    def call_search(self, search_request_body):
        # Placeholder for actual API call to Beckn registry or protocol endpoint
        url = "https://mock_bpp.com/beckn/mobility/search"  # BPP endpoint
        headers = Helper.construct_auth_header(search_request_body)
        response = requests.post(url, json=search_request_body, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error with the search request")

    @staticmethod
    def create_context(transaction_id):
        return {
            "domain": "nic2004:60221",
            "country": "IND",
            "city": "std:080",
            "action": "search",
            "core_version": "0.9.1",
            "bap_id": "http://localhost:3000/",  # BAP (client) URI
            "bap_uri": "http://localhost:3000/beckn/",  # BAP (client) URI
            "transaction_id": transaction_id,
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
