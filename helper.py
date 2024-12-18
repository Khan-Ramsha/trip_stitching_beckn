from datetime import datetime
import uuid
import hashlib
import hmac
import json

class Helper:
    @staticmethod
    def create_context(transaction_id):
        # Generates context with a given transaction ID
        return {
            "domain": "nic2004:60221",
            "country": "IND",
            "city": "std:080",
            "action": "search",
            "core_version": "0.9.1",
            "bap_id": "df35-203-192-239-167.ngrok-free.app",  # BAP (client) URI
            "bap_uri": "https://df35-203-192-239-167.ngrok-free.app",  # BAP (client) URI
            "transaction_id": transaction_id,
            "message_id": str(uuid.uuid4()),  # Dynamically generate message_id
            "timestamp": datetime.utcnow().isoformat() + 'Z'  # Dynamic timestamp
        }

    @staticmethod
    def generate_search_request(pickup, drop, catalogs, optimization_parameter):
        timestamp = datetime.utcnow().isoformat()
        transaction_id = str(uuid.uuid4())  # Unique transaction ID for each request
        context = Helper.create_context(transaction_id)  # Calling the static method with the class reference

        return {
            "context": context,  # Use dynamically generated context
            "message": {
                "intent": {
                    "fulfillment": {
                        "start": {"location": {"gps": pickup}},
                        "end": {"location": {"gps": drop}}
                    }
                }
            }
        }
    
    def construct_auth_header(request_body):
        secret_key = "a65788a9-598e-4088-85c1-1934e9a9f7a0"
        message = json.dumps(request_body, separators=(',', ':'))
        signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bearer {signature}"}
