import time
import datetime
import os
from trip_plan import TripPlan
from journey import Journey

start_time=time.time()

api_key      = os.environ['API_KEY']
service      = os.environ['SERVICE']
origin       = os.environ['ORIGIN']
destination  = os.environ['DESTINATION']
current_journey_ids = []

while True:
    print('-> ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    trip = TripPlan(service, origin, destination, api_key)
    journey_id = trip.next_journey_id()
    if journey_id is None:
        print('Error fetching journey. Skipping')
    else:
        if journey_id not in current_journey_ids:
            current_journey_ids.append(journey_id)
            print('=> Added journey: ' + journey_id)

    for journey_id in current_journey_ids:
        print ('(journey id: ' + journey_id +')')

        journey = Journey(journey_id, api_key)
        if journey.has_stops_info():
            journey.print()
            if journey.finished():
                current_journey_ids.remove(journey_id)
                journey.to_csv()
                print('=> Destination reached')
        else:
            print('Error with the journey data. Skipping')

    time.sleep(60.0 - ((time.time() - start_time) % 60.0))


