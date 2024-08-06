import json
import os
import requests

# Paths to your .crt and .key files
cert_file = '/betfair/client-2048.crt'  # Your .crt file
key_file = '/betfair/client-2048.key'    # Your .key file

# Betfair's login URL for certificate-based API access
login_url = 'https://identitysso-cert.betfair.com/api/certlogin'

# Your Betfair username and password
payload = {
    'username': os.getenv('BETFAIR_USERNAME'),
    'password': os.getenv('BETFAIR_PASSWORD')
}

headers = {
    'X-Application' : os.getenv('BETFAIR_APPLICATION_KEY'),
}

url_prefix = 'https://api.betfair.com/exchange/betting/rest/v1.0/'

PREMIER_LEAGUE_ID = 10932509
CHAMPIONSHIP_ID = 7129730
LEAGUE_ONE_ID = 35
LEAGUE_TWO_ID = 37
NATIONAL_LEAGUE_ID = 11086347

FOOTBALL_EVENT_ID = 1

# Perform the login request
try:
    response = requests.post(login_url, data=payload, cert=(cert_file, key_file), headers=headers)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Assuming successful login, print the session token
        session_token = response.json().get('sessionToken')
        headers['X-Authentication'] = session_token
        headers['content-type'] = 'application/json'
        print(f"Login successful! Session Token: {session_token}")
        print(headers)

        football_and_weekend_filter = json.dumps({
            "filter": {
                "eventTypeIds": [FOOTBALL_EVENT_ID],
                "marketStartTime": {
                    "from": "2024-08-09T00:00:00Z",
                    "to": "2024-08-12T23:59:59Z"
                }
            }
        })
        football_weekend_and_competition_filter = json.dumps({
            "filter": {
                "eventTypeIds": [FOOTBALL_EVENT_ID],
                "competitionIds": [CHAMPIONSHIP_ID, LEAGUE_ONE_ID, LEAGUE_TWO_ID],
                "marketStartTime": {
                    "from": "2024-08-09T00:00:00Z",
                    "to": "2024-08-12T23:59:59Z"
                }
            }
        })

        list_competitions_endpoint = url_prefix + 'listCompetitions/'
        list_events_endpoint = url_prefix + 'listEvents/'

        response = requests.post(list_events_endpoint, data=football_weekend_and_competition_filter, headers=headers)
        json_response = sorted(json.loads(response.text), key=lambda x: x['event']['openDate'])
        print(json.dumps(json_response, indent=3))
        output = "\n".join([f"{event['event']['id']},{event['event']['name']}" for event in json_response])

        print(output)

        LEEDS_PORTSMOUTH_ID = 33375220

        # response = requests.post(list_competitions_endpoint, data=football_and_weekend_filter, headers=headers)
        # print(json.dumps(json.loads(response.text), indent=3))

        markets_for_a_game_filter = json.dumps({
            "filter": {
                "eventIds": [LEEDS_PORTSMOUTH_ID],
                # "marketBettingTypes": ["ASIAN_HANDICAP_DOUBLE_LINE"],
            },
            "maxResults": 200,
            "marketProjection": [
                "RUNNER_DESCRIPTION",
                "RUNNER_METADATA"
            ]
        })
        list_market_catalogue_endpoint = url_prefix + 'listMarketCatalogue/'

        response = requests.post(list_market_catalogue_endpoint, data=markets_for_a_game_filter, headers=headers)
        print(json.dumps(json.loads(response.text), indent=3))

        book_filter = json.dumps({
            "marketIds": ["1.230168138"],
            "priceProjection": {
                "priceData": ["EX_BEST_OFFERS"],
                "keyLineDescription": True
            }
        })
        list_market_book_endpoint = url_prefix + 'listMarketBook/'

        response = requests.post(list_market_book_endpoint, data=book_filter, headers=headers)
        print(json.dumps(json.loads(response.text), indent=3))

    else:
        print(f"Login failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


