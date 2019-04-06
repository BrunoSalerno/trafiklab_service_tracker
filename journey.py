import requests
import datetime
import time
import itertools
import os
import csv

class Journey(object):
    def __init__(self, journey_id, api_key):
        self.api_key = api_key
        self.journey_id = journey_id
        self.stops = None
        self.name = None
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
        if 'Names' in data:
            self.name = data['Names']['Name'][0]

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
            return False

    def build_headers(self, stop):
        headers = []
        sname = stop['name'].replace(' ','_')
        if 'arrTime' in stop:
            headers = headers + [sname + '_arrTime', sname + '_rtArrTime']
        if 'depTime' in stop:
            headers = headers + [sname + '_depTime', sname + '_rtDepTime']
        return headers

    def build_fields(self, stop):
        fields = []
        if 'arrTime' in stop:
            fields = fields + [stop['arrTime'], stop['rtArrTime']]
        if 'depTime' in stop:
            fields = fields + [stop['depTime'], stop['rtDepTime']]
        return fields

    def to_csv(self):
        filename = self.name['name'].replace(' ','_') + '.csv'
        headers = ['journey_id'] + list(itertools.chain(*map(self.build_headers,self.stops)))
        row = [self.journey_id] + list(itertools.chain(*map(self.build_fields,self.stops)))

        mode = 'w'
        if os.path.isfile(filename):
            mode = 'a'

        with open(filename, mode) as f:
            writer = csv.writer(f)
            if mode == 'w':
                writer.writerow(headers)
            writer.writerow(row)
