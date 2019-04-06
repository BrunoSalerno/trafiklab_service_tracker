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

def trip_url(orig_id,dest_id):
    return 'https://api.sl.se/api2/TravelplannerV3_1/trip.json?key=' + api_key + '&lang=en&originExtId=' + orig_id + '&destExtId=' + dest_id

def journey_detail_url(journey_id):
    return 'https://api.sl.se/api2/TravelplannerV3_1/journeydetail.json?key=' + api_key + '&id=' + journey_id

def find_trip(product_name,trips):
    for trip in trips:
        legs = trip['LegList']['Leg']
        for leg in legs:
            if leg['Product']['name'] == product_name:
                return leg

def fetch_new_journey_id(product_name, orig, dest):
    trip_data = requests.get(trip_url(origin,dest))
    trips = trip_data.json()
    trip = find_trip(product_name,trips['Trip'])
    return trip['JourneyDetailRef']['ref']


# Every one minute I fetch the data for the current_journey_id
# If the last stop has been reached, I fetch a new journey_id

while True:
    print('-> ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    if current_journey_id is None:
        current_journey_id = fetch_new_journey_id(service, origin, destination)
        print('=> New journey: ' + current_journey_id)
    else:
        print ('(current journey id: ' + current_journey_id +')')

    journey_data = requests.get(journey_detail_url(current_journey_id))
    journey = journey_data.json()

    if not 'Stops' in journey:
        print('Error with the response. Skipping')
        continue

    stops = journey['Stops']['Stop']

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

    last_stop = stops[-1]
    if 'rtArrTime' in last_stop:
        t = datetime.datetime.strptime(last_stop['rtArrTime'] + ' ' + last_stop['rtArrDate'], "%H:%M:%S %Y-%m-%d")
        if t.timestamp() < time.time():
            current_journey_id = None
            print('=> Destination reached')

    time.sleep(60.0 - ((time.time() - start_time) % 60.0))


