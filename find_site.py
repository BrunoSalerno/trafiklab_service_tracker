from utils.get_with_retry import get_with_retry
import os
import sys

api_key     = os.environ['API_KEY']
place_name  = ' '.join(sys.argv[1:])
max_results = '10'

if not place_name:
    print("Missing place arg. Exiting")

url = 'https://api.sl.se/api2/typeahead.json?key=' + api_key + '&searchstring=' + place_name + '&maxresults=' + max_results

res = get_with_retry(url)
data = res.json()

print('Place name: Site Id')
print('-------------------')
for place in data['ResponseData']:
    print(place['Name'] + ': ' + place['SiteId'])
