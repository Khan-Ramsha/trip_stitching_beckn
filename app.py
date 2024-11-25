from flask import Flask, request, jsonify
from mobility_service import MobilityService

app = Flask(__name__)

# Create instance of the MobilityService
mobility_service = MobilityService()

# Route to search for trips 
@app.route('/mobility/search', methods=['POST'])
def search():
    try:
        # Get data from the user
        data = request.get_json()
        pickup = data['pickup']  # Pick location
        drop = data['drop']  # Destination
        catalogs = data['catalogs']  # List of mobility catalogs (e.g., ride-hailing, rentals)
        optimization_parameter = data['optimization_parameter']  # Either cost or distance

        # Use MobilityService to handle the search
        search_response = mobility_service.process_search(pickup, drop, catalogs, optimization_parameter)

        # Return the raw search response from BAP server
        return jsonify(search_response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle the on_search logic (trip stitching)
@app.route('/mobility/on_search', methods=['POST'])
def on_search():
    try:
        # Get search response from the request
        data = request.get_json()
        search_response = data['search_response']  # Raw response from the previous search route
        optimization_parameter = data['optimization_parameter']  # Either cost or distance

        # Use MobilityService to handle the stitching
        stitched_trips = mobility_service.process_on_search(search_response, optimization_parameter)

        # Return the stitched trips
        return jsonify(stitched_trips), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
