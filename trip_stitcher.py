class TripStitcher:
    def perform_trip_stitching(self, search_response, optimization_parameter):
        trips = []
        # Process the mobility catalogs and stitch the trips
        for provider in search_response.get('message', {}).get('catalog', {}).get('bpp/providers', []):
            provider_name = provider['descriptor']['name']
            for item in provider.get('items', []):
                trip = {
                    "provider": provider_name,
                    "vehicle_type": item['descriptor']['name'],
                    "price": item['price']['value'],
                    "duration": item['time']['duration'],
                    "gps": item['location_id'],
                    "optimization_parameter": optimization_parameter
                }
                trips.append(trip)

        # Sort trips based on the optimization parameter (e.g., cost, distance)
        if optimization_parameter == 'cost':
            trips.sort(key=lambda x: x['price'])
        elif optimization_parameter == 'distance':
            trips.sort(key=lambda x: x['duration'])  # Assuming duration as a proxy for distance

        return trips
