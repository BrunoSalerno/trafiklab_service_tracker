# trafiklab_service_tracker

This tool fetches information about current journeys of a given transit route using the TrafikLab APIs. The data is only available for Stockholm, Sweden.
The script logs every one minute the expected and actual time of departure/arrival by stop, for all the current journeys of the route. When each journey finishes, its final values are appended to a CSV file.

## Usage
```
API_KEY=<Your API key> SERVICE="Bus 550" ORIGIN=9703 DESTINATION=5889 pipenv run python main.py
```

The api key is the one for the Trafiklab's [TravelPlanner V3.1 API](https://www.trafiklab.se/api/sl-reseplanerare-31).
The ids of origins and destinations can be fetched with the Trafiklab's [Platsuppslag API](https://www.trafiklab.se/api/sl-platsuppslag/dokumentation).
