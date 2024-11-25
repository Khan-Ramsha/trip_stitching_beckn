from beckn_search import BecknSearch
from trip_stitcher import TripStitcher

class MobilityService:
    def __init__(self):
        self.beckn_search = BecknSearch()
        self.trip_stitcher = TripStitcher()

    def process_search(self, pickup, drop, catalogs, optimization_parameter):
        # Generates the protocol request body
        search_request = self.beckn_search.generate_search_request(pickup, drop, catalogs, optimization_parameter)

        # BAP server calls protocol search to the network
        search_response = self.beckn_search.call_search(search_request)

        # Return search response without stitching
        return search_response

    def process_on_search(self, search_response, optimization_parameter):
        # Perform trip stitching based on search response
        stitched_trips = self.trip_stitcher.perform_trip_stitching(search_response, optimization_parameter)
        return stitched_trips
