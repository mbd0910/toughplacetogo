from __future__ import annotations
import json
import os
import requests
from match_odds import MatchOdds
from odds import Odds

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

MARKET_ID_KEY = 'marketId'
MARKET_NAME_KEY = 'marketName'
RUNNERS_KEY = 'runners'
RUNNER_NAME_KEY = 'runnerName'
SELECTION_ID_KEY = 'selectionId'

ASIAN_HANDICAP_MARKET_NAME = 'Asian Handicap'
GOAL_LINE_MARKET_NAME = 'Goal Lines'
BTTS_MARKET_NAME = 'Both teams to Score?'
MATCH_ODDS_MARKET_NAME = 'Match Odds'
OVER_UNDER_2_POINT_5_GOALS_MARKET_NAME = 'Over/Under 2.5 Goals'
CORRECT_SCORE_MARKET_NAME = 'Correct Score'

def main():
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
            # TODO: get these from the game name, split on the 'v'
            home_team_name = 'Leeds'
            away_team_name = 'Portsmouth'

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
            json_response = json.loads(response.text)
            markets = "\n".join([f"{market[MARKET_ID_KEY]},{market[MARKET_NAME_KEY]}" for market in json_response])
            print(markets)

            for market in json_response:
                if market[MARKET_NAME_KEY] == MATCH_ODDS_MARKET_NAME:
                    match_odds = get_match_odds(market, home_team_name, away_team_name)
                    print(match_odds)

        else:
            print(f"Login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def get_match_odds(market, home_team_name, away_team_name):
    match_odds_market_id = market[MARKET_ID_KEY]
    selections_by_id = {}

    for selection in market[RUNNERS_KEY]:
        selections_by_id[selection[SELECTION_ID_KEY]] = selection

    book_filter = json.dumps({
        "marketIds": [match_odds_market_id],
        "priceProjection": {
            "priceData": ["EX_BEST_OFFERS"],
            "keyLineDescription": True
        }
    })
    list_market_book_endpoint = url_prefix + 'listMarketBook/'

    match_odds_response = requests.post(list_market_book_endpoint, data=book_filter, headers=headers)
    match_odds = json.loads(match_odds_response.text)
    match_odds_result = MatchOdds()

    print(json.dumps(match_odds, indent=3))

    for selection_book in match_odds[0][RUNNERS_KEY]:
        selection_id = selection_book[SELECTION_ID_KEY]
        runner_name = selections_by_id[selection_id][RUNNER_NAME_KEY]

        best_back = selection_book['ex']['availableToBack'][0]['price']
        best_lay = selection_book['ex']['availableToLay'][0]['price']
        best_price = Odds((best_back + best_lay) / 2)

        if runner_name == home_team_name:
            match_odds_result.home = best_price
        elif runner_name == away_team_name:
            match_odds_result.away = best_price
        else:
            match_odds_result.draw = best_price

    return match_odds_result



main()
