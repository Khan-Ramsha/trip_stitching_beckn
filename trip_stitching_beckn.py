# # from flask import Flask, request, jsonify
# # import requests

# # app = Flask(__name__)

# # # Temporary storage for callback responses (for simplicity)
# # routes_storage = {}

# # # Endpoint 1: /search - To initiate the trip search
# # @app.route('/search', methods=['POST'])
# # def search_trip():
# #     try:
# #         # Get input data from the user request
# #         data = request.get_json()
# #         pickup = data['pickup']
# #         drop = data['drop']
# #         catalogs = data['catalogs']  # e.g., ["public transit", "rentals"]
# #         optimization_param = data['optimization_param']  # 'cost' or 'distance'
# #         client_callback_url = data['client_callback_url']  # The callback URL to receive results

# #         # Send request to BAP
# #         bap_request_data = {
# #             "pickup": pickup,
# #             "drop": drop,
# #             "catalogs": catalogs,
# #             "optimization_param": optimization_param,
# #             "client_callback_url": client_callback_url  # Include client callback in request
# #         }

# #         # Assuming the BAP API is running at localhost:5000/bap_search
# #         bap_url = "http://localhost:5000/search"  # Adjust BAP URL as needed
# #         response = requests.post(bap_url, json=bap_request_data)

# #         # If BAP responds successfully
# #         if response.status_code == 200:
# #             return jsonify({"message": "Request sent to BAP successfully"}), 200
# #         else:
# #             return jsonify({"error": "Failed to send request to BAP"}), response.status_code

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500


# # # Endpoint 2: /client_callback - To process the BAP's response
# # @app.route('/client_callback', methods=['POST'])
# # def client_callback():
# #     try:
# #         # Receive the routes data from BAP
# #         bap_data = request.get_json()

# #         # Extract the optimization parameter from the request
# #         optimization_param = bap_data.get('optimization_param', 'cost')  # Default to 'cost'

# #         # Extract routes from BAP response
# #         routes = bap_data.get('routes', [])
# #         if not routes:
# #             return jsonify({"error": "No routes provided by BAP"}), 400

# #         # Sort routes based on optimization parameter (either cost or distance)
# #         sorted_routes = sorted(routes, key=lambda x: x.get(optimization_param, float('inf')))

# #         # Store sorted routes for demonstration purposes (or return directly)
# #         request_id = bap_data.get('request_id', 'default')  # Optional: Track requests
# #         routes_storage[request_id] = sorted_routes

# #         # Respond with sorted routes (can also call back to the client system)
# #         return jsonify(sorted_routes), 200

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500


# # # For testing, retrieve sorted routes from storage
# # @app.route('/get_sorted_routes', methods=['GET'])
# # def get_sorted_routes():
# #     try:
# #         request_id = request.args.get('request_id', 'default')
# #         sorted_routes = routes_storage.get(request_id, [])
# #         return jsonify(sorted_routes), 200
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500


# # if __name__ == '__main__':
# #     app.run(debug=True)



# from flask import Flask, request, jsonify
# import networkx as nx
# import numpy as np
# import random

# app = Flask(__name__)

# # Simulate fetching mobility data (e.g., ride-hailing, public transit)
# def fetch_mobility_routes(pickup, drop, catalogs, optimization_param):
#     # Simulating data fetching from different catalogs (e.g., Uber, Ola, Bus)
#     routes = []
#     for catalog in catalogs:
#         # Simulate random data for distance and cost
#         distance = random.randint(5, 50)  # Random distance in km
#         cost = random.randint(50, 300)  # Random cost in INR
#         routes.append({
#             "catalog": catalog,
#             "pickup": pickup,
#             "drop": drop,
#             "distance": distance,
#             "cost": cost
#         })
#     return routes

# # Define the trip stitching logic
# def trip_stitching_algorithm(pickup, drop, catalogs, optimization_param="distance"):
#     # Step 1: Fetch routes from mobility catalogs
#     routes = fetch_mobility_routes(pickup, drop, catalogs, optimization_param)
    
#     # Step 2: Create a directed graph to represent the routes
#     G = nx.DiGraph()
    
#     # Add routes to the graph
#     for route in routes:
#         G.add_edge(route["pickup"], route["drop"], distance=route["distance"], cost=route["cost"])
    
#     # Step 3: Find all possible paths between pickup and drop
#     all_paths = list(nx.all_simple_paths(G, source=pickup, target=drop))
    
#     # Step 4: Rank the paths based on the optimization parameter (e.g., distance or cost)
#     if optimization_param == "distance":
#         all_paths = sorted(all_paths, key=lambda path: sum(G[u][v]['distance'] for u, v in zip(path[:-1], path[1:])))
#     elif optimization_param == "cost":
#         all_paths = sorted(all_paths, key=lambda path: sum(G[u][v]['cost'] for u, v in zip(path[:-1], path[1:])))
    
#     return all_paths

# @app.route('/search', methods=['POST'])
# def search():
#     """
#     Search for multi-modal trip options.
#     User sends a request with pickup, drop, catalogs, and optimization parameter.
#     """
#     data = request.get_json()
#     pickup = data['pickup']
#     drop = data['drop']
#     catalogs = data['catalogs']  # List of mobility catalogs (e.g., 'ride-hailing', 'public_transit')
#     optimization_param = data.get('optimization_param', 'distance')  # Default is distance
    
#     # Run the trip stitching algorithm to find paths
#     stitched_paths = trip_stitching_algorithm(pickup, drop, catalogs, optimization_param)
    
#     # Return the resulting paths
#     return jsonify({"paths": stitched_paths})

# @app.route('/client_callback', methods=['POST'])
# def client_callback():
#     """
#     The BAP sends a callback to the client with the available routes or other relevant details.
#     """
#     data = request.get_json()
    
#     # Simulating a callback that confirms the availability of routes
#     # Normally, this would contain the response from the mobility providers.
#     status = "success"  # Here you can define success or failure based on actual logic
#     message = "Routes found and available for the requested trip."
    
#     return jsonify({"status": status, "message": message, "data": data})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import requests
import uuid
from datetime import datetime
import hashlib
import hmac
import json

app = Flask(__name__)

# Helper functions for generating context, headers, and lookup
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

def construct_auth_header(request_body):
    # This is a simple placeholder. You'll want to generate a digital signature for the request
    secret_key = "your_secret_key"
    message = json.dumps(request_body, separators=(',', ':'))
    signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {"Authorization": f"Bearer {signature}"}

def lookup():
    # This function returns the BPP URI where the network (mobility service) is hosted
    return "http://localhost:7000"  # BPP (network) URI

# Route to trigger the search
@app.route('/mobility/search_by_pickup_drop_location', methods=['POST'])
def search_by_loc():
    try:
        body = request.get_json()
        transaction_id = str(uuid.uuid4())  # Unique transaction ID for each request
        context = create_context(transaction_id)
        
        # Create the request body for the protocol search
        search_request_body = {
            "context": context,
            "message": {
                "intent": {
                    "fulfillment": {
                        "start": {
                            "location": {
                                "gps": body["pickup_location"]
                            }
                        },
                        "end": {
                            "location": {
                                "gps": body["drop_location"]
                            }
                        }
                    }
                }
            }
        }

        # Send the request to the BPP (protocol network)
        response = call_search(search_request_body)

        # Respond to the client
        return jsonify(response), 200

    except Exception as error:
        return jsonify({"status": "NACK", "error": str(error)}), 500

def call_search(search_request_body):
    uri = lookup()  # Get the URI for the BPP (protocol network)
    headers = construct_auth_header(search_request_body)
    # Send the POST request to the BPP's /mobility/search endpoint
    response = requests.post(f"{uri}/mobility/search", json=search_request_body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error with the search request")

# Route for handling the search result (on_search)
@app.route('/mobility/on_search', methods=['POST'])
def on_search():
    try:
        body = request.get_json()
        # In this example, we're simply returning the received search results
        return jsonify({"status": "ACK", "data": body}), 200
    except Exception as error:
        return jsonify({"status": "NACK", "error": str(error)}), 500

# Route for client to poll the search results
@app.route('/mobility/get_message_by_id', methods=['GET'])
def get_message_by_id():
    try:
        message_id = request.args.get("messageId")
        if not message_id:
            raise ValueError("Missing messageId")
        
        # Mocked response, in reality, this would come from a stored message
        result = {"message_id": message_id, "data": "Sample data for messageId"}
        return jsonify({"status": "ACK", "data": result}), 200

    except Exception as error:
        return jsonify({"status": "NACK", "error": str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7000)  # Ensure the BAP (server) is running on port 7000