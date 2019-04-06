import requests
import time
import datetime
import os

start_time=time.time()

api_key      = os.environ['API_KEY']
service      = os.environ['SERVICE']
origin       = os.environ['ORIGIN']
destination  = os.environ['DESTINATION']
current_journey_id  = None

class MissingJourney(Exception):
    pass

def trip_url(orig_id,dest_id):
    return 'https://api.sl.se/api2/TravelplannerV3_1/trip.json?key=' + api_key + '&lang=en&originExtId=' + orig_id + '&destExtId=' + dest_id

def journey_detail_url(journey_id):
    return 'https://api.sl.se/api2/TravelplannerV3_1/journeydetail.json?key=' + api_key + '&id=' + journey_id

def find_trip(product_name,trips):
    for trip in trips:
        legs = trip['LegList']['Leg']
        for leg in legs:
            if 'Product' not in leg:
                raise MissingJourney()
            if leg['Product']['name'] == product_name:
                return leg

def fetch_new_journey_id(product_name, orig, dest):
    trip_data = requests.get(trip_url(origin,dest))
    trips = trip_data.json()
    trip = find_trip(product_name,trips['Trip'])
    if trip is None:
        raise MissingJourney()
    return trip['JourneyDetailRef']['ref']

def fetch_journey(journey_id):
    res = requests.get(journey_detail_url(journey_id))
    return res.json()

def print_stops_data(stops):
    for stop in stops:
        print('> ' + stop['name'])
        if 'arrTime' in stop:
            if 'rtArrTime' in stop:
                print('arrTime: ' + stop['arrTime'] + ' | rtArrTime: ' + stop['rtArrTime'])
            else:
                print('no realtime info right now for arrivals')
        if 'depTime' in stop:
            if 'rtDepTime' in stop:
                print('depTime: ' + stop['depTime'] + ' | rtDepTime: ' + stop['rtDepTime'])
            else:
                print('no realtime info right now for depatures')

def last_stop_reached(stops):
    last_stop = stops[-1]
    if 'rtArrTime' in last_stop:
        t = datetime.datetime.strptime(last_stop['rtArrTime'] + ' ' + last_stop['rtArrDate'], "%H:%M:%S %Y-%m-%d")
        return t.timestamp() < time.time()
    else:
        return false

# Every one minute I fetch the data for the current_journey_id
# If the last stop has been reached, I fetch a new journey_id

while True:
    print('-> ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    if current_journey_id is None:
        try:
            current_journey_id = fetch_new_journey_id(service, origin, destination)
            print('=> New journey: ' + current_journey_id)
        except MissingJourney:
            print('Error fetching journey. Skipping')
    else:
        print ('(current journey id: ' + current_journey_id +')')

    if current_journey_id is not None:
        journey = fetch_journey(current_journey_id)
        if 'Stops' in journey:
            stops = journey['Stops']['Stop']
            print_stops_data(stops)
            if last_stop_reached(stops):
                current_journey_id = None
                print('=> Destination reached')
        else:
            print('Error with the journey data. Skipping')

    time.sleep(60.0 - ((time.time() - start_time) % 60.0))


