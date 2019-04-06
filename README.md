# trafiklab_service_tracker

This tool fetches current journeys information from TrafikLab APIs. The information is only available for Stockholm, Sweden.

## Usage
```
API_KEY=<Your API key> SERVICE="Bus 550" ORIGIN=9703 DESTINATION=5889 pipenv run python main.py
```

The api key is the one for the Trafiklab's [TravelPlanner V3.1 API](https://www.trafiklab.se/api/sl-reseplanerare-31).
The ids of origins and destiantions can be fetch by using the Trafiklab's [Platsuppslag API](https://www.trafiklab.se/api/sl-platsuppslag/dokumentation)
