import time
import datetime
import os
from lib.trip_plan import TripPlan
from lib.journey import Journey

start_time=time.time()

api_key      = os.environ['API_KEY']
service      = os.environ['SERVICE']
origin       = os.environ['ORIGIN']
destination  = os.environ['DESTINATION']
journeys = {}

min_freq = 1
if 'FREQ' in os.environ:
    min_freq = int(os.environ['FREQ'])

sec_freq = min_freq * 60.0

print("Tracking " + service + ", from " + origin + " to " + destination)
print("Iteration every " + str(min_freq) + " minutes")
print("To stop, press Ctrl+C")
print("-----------------------------------------")

while True:
    print('=> ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    trip = TripPlan(service, origin, destination, api_key)
    journey_id = trip.next_journey_id()
    if journey_id is None:
        print('Error fetching journey. Skipping')
    else:
        if journey_id not in journeys:
            journeys[journey_id] = Journey(journey_id, api_key)

    print('-> Tracking journeys: ' + ', '.join(list(journeys.keys())))

    for journey_id, journey in journeys.copy().items():
        now = time.time()
        if not journey.expected_finish_time() or now > journey.expected_finish_time():
            if journey.expected_finish_time():
                print('Journey ' + journey_id + ' should have finished. Checking')
            if journey.refresh():
                if journey.finished():
                    del journeys[journey_id]
                    journey.to_csv()
                    print('-> Journey ' + journey_id + ' finished')
                else:
                    # The following code remove old journeys with no realtime info
                    if not journey.expected_finish_time() and now > journey.scheduled_finish_time():
                        del journeys[journey_id]
                        print('Stop tracking journey' + journey_id + ', which does not have realtime data')
            else:
                print('Error with the journey data. Skipping')

    time.sleep(sec_freq - ((time.time() - start_time) % sec_freq))
