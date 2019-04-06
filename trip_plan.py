import requests

class TripPlan(object):
    def __init__(self, service, orig, dest, api_key):
        self.api_key = api_key
        self.service = service
        self.orig = orig
        self.dest = dest
        self.load()

    def url(self):
        return 'https://api.sl.se/api2/TravelplannerV3_1/trip.json?key=' + self.api_key + '&lang=en&originExtId=' + self.orig + '&destExtId=' + self.dest

    def load(self):
        res = requests.get(self.url())
        self.trips = res.json()['Trip']

    def next_trip(self):
        for trip in self.trips:
            legs = trip['LegList']['Leg']
            for leg in legs:
                if 'Product' not in leg:
                    continue
                if leg['Product']['name'] == self.service:
                    return leg

    def next_journey_id(self):
        trip = self.next_trip()
        if trip is None:
            return None
        return trip['JourneyDetailRef']['ref']