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

        football_and_friday_filter = '{"filter":{ "eventTypeIds": ["1"], "marketStartTime": {"from": "2024-08-05T00:00:00Z","to": "2024-08-05T23:59:59Z"}}}'
        list_events_endpoint = url_prefix + 'listEvents/'

        response = requests.post(list_events_endpoint, data=football_and_friday_filter, headers=headers)
        print(json.dumps(json.loads(response.text), indent=3))

        # individual_filter = '{"filter":{ "eventIds": ["33464179"], "marketBettingTypes": ["ASIAN_HANDICAP_DOUBLE_LINE"]}, "maxResults": "200", "marketProjection": ["RUNNER_DESCRIPTION", "RUNNER_METADATA"]}'
        individual_filter = '{"filter":{ "eventIds": ["33464179"], "maxResults": "200", "marketProjection": ["RUNNER_DESCRIPTION", "RUNNER_METADATA"]}'
        list_market_catalogue_endpoint = url_prefix + 'listMarketCatalogue/'

        response = requests.post(list_market_catalogue_endpoint, data=individual_filter, headers=headers)
        print(json.dumps(json.loads(response.text), indent=3))

        market_filter = '{"marketIds":["1.231381167"],"priceProjection":{"priceData":["EX_BEST_OFFERS"], "keyLineDescription": true}}'
        list_market_book_endpoint = url_prefix + 'listMarketBook/'

        response = requests.post(list_market_book_endpoint, data=market_filter, headers=headers)
        print(json.dumps(json.loads(response.text), indent=3))

    else:
        print(f"Login failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


