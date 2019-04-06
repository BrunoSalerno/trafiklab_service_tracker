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
current_journey_id  = None

# Every one minute I fetch the data for the current_journey_id
# If the last stop has been reached, I fetch a new journey_id

while True:
    print('-> ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    if current_journey_id is None:
        trip = TripPlan(service, origin, destination, api_key)
        current_journey_id = trip.next_journey_id()
        if current_journey_id is None:
            print('Error fetching journey. Skipping')
        else:
            print('=> New journey: ' + current_journey_id)
    else:
        print ('(current journey id: ' + current_journey_id +')')

    if current_journey_id is not None:
        journey = Journey(current_journey_id, api_key)
        if journey.has_stops_info():
            journey.print()
            if journey.finished():
                journey.to_csv()
                current_journey_id = None
                print('=> Destination reached')
        else:
            print('Error with the journey data. Skipping')

    time.sleep(60.0 - ((time.time() - start_time) % 60.0))


