import requests
import datetime
import time

class Journey(object):
    def __init__(self, journey_id, api_key):
        self.api_key = api_key
        self.journey_id = journey_id
        self.stops = None
        self.load()

    def has_stops_info(self):
        return self.stops is not None

    def url(self):
        return 'https://api.sl.se/api2/TravelplannerV3_1/journeydetail.json?key=' + self.api_key + '&id=' + self.journey_id

    def load(self):
        res = requests.get(self.url())
        data = res.json()
        if 'Stops' in data:
            self.stops = data['Stops']['Stop']

    def print(self):
        for stop in self.stops:
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

    def finished(self):
        last_stop = self.stops[-1]
        if 'rtArrTime' in last_stop:
            t = datetime.datetime.strptime(last_stop['rtArrTime'] + ' ' + last_stop['rtArrDate'], "%H:%M:%S %Y-%m-%d")
            return t.timestamp() < time.time()
        else:
            return false
