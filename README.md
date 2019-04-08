# trafiklab_service_tracker

This tool fetches information about current journeys of a given transit route using the [TrafikLab APIs](https://www.trafiklab.se/api). The data is only available for Stockholm, Sweden.
The script logs every one minute the expected and actual time of departure/arrival by stop, for all the current journeys of the route. When each journey finishes, its final values are appended to a CSV file.

## Setup
- Install `pipenv`
- Clone/download this repository
- Inside the folder, run `pipenv install`
- Fetch the API keys from Trafiklab (see below).

## Usage
```
API_KEY=<Your API key> SERVICE="Bus 550" ORIGIN=9703 DESTINATION=5889 pipenv run python main.py
```

The api key is the one for the Trafiklab's [TravelPlanner V3.1 API](https://www.trafiklab.se/api/sl-reseplanerare-31).
The ids of origins and destinations can be fetched with the Trafiklab's [Platsuppslag API](https://www.trafiklab.se/api/sl-platsuppslag/dokumentation), which can be done directly with the `find_site` script included in this repo (see next).

## find_site script
This script allows you to find the `site_id` of any place in Stockholm. To use it, you need the [Platsuppslag API](https://www.trafiklab.se/api/sl-platsuppslag/dokumentation) key.

```
API_KEY=<Your API key> pipenv run python find_site.py Stora Torget
```

## API keys
To get your API keys, you have to create a project in [Trafiklab](https://www.trafiklab.se), enable the desires APIs, and generate the keys.
