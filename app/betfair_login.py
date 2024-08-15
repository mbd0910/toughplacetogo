from __future__ import annotations
import json
import os
import requests
from match_odds import MatchOdds
from odds import Odds
from asian_handicap_odds import AsianHandicapOdds
from total_goals_odds import TotalGoalsOdds
from poisson_minimisation import calculate_scoreline_distribution, find_expected_goals
from calculate_expected_team_points import calculate_expected_home_team_points, calculate_expected_away_team_points
from efl_game_prediction import EFLGamePrediction
from efl_gameweek_prediction import EFLGameweekPrediction
from betfair_event import BetfairEvent
from datetime import datetime, timezone
from moneyed import Money, GBP
from decouple import config

# Paths to your .crt and .key files
cert_file = config('BETFAIR_CERT_PATH') # '/betfair/client-2048.crt'  # Your .crt file
key_file = config('BETFAIR_KEY_PATH') # /betfair/client-2048.key'    # Your .key file

# Betfair's login URL for certificate-based API access
login_url = 'https://identitysso-cert.betfair.com/api/certlogin'

# Your Betfair username and password
payload = {
    'username': config('BETFAIR_USERNAME'),
    'password': config('BETFAIR_PASSWORD')
}

headers = {
    'X-Application' : config('BETFAIR_APPLICATION_KEY'),
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
TOTAL_MATCHED_KEY = 'totalMatched'
RUNNERS_KEY = 'runners'
RUNNER_NAME_KEY = 'runnerName'
SELECTION_ID_KEY = 'selectionId'
KEY_LINE_DESCRIPTION_KEY = 'keyLineDescription'
KEY_LINE_KEY = 'keyLine'

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

            football_weekend_and_competition_filter = json.dumps({
                "filter": {
                    "eventTypeIds": [FOOTBALL_EVENT_ID],
                    "competitionIds": [CHAMPIONSHIP_ID, LEAGUE_ONE_ID, LEAGUE_TWO_ID],
                    "marketStartTime": {
                        "from": "2024-08-16T00:00:00Z",
                        "to": "2024-08-19T23:59:59Z"
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

            efl_gameweek_prediction = EFLGameweekPrediction()

            for event in json_response:
                event_name = event['event']['name']

                if (event_name != 'English Championship' and
                        event_name != 'English League 1' and
                        event_name != 'English League 2'):
                    efl_game_prediction = process_event(event)

                    if efl_game_prediction:
                        efl_gameweek_prediction.add_game_prediction(efl_game_prediction)

                        print(efl_game_prediction.betfair_event.event_name)
                        print(f"Home expected goals/points: {efl_game_prediction.expected_goals.home} -> {efl_game_prediction.expected_home_points}")
                        print(f"Away expected goals/points: {efl_game_prediction.expected_goals.away} -> {efl_game_prediction.expected_away_points}")
                    else:
                        print(f"No prediction yet for {event_name}")

            for game_prediction, team, sort_by_value in efl_gameweek_prediction.sort_teams_by_points():
                # type: EFLGamePrediction, str, float
                kickoff = game_prediction.betfair_event.kickoff
                home_or_away = 'HOME' if game_prediction.is_home_team(team) else 'AWAY'

                print(",".join([
                    kickoff.strftime('%d-%m-%Y %H:%M'),
                    home_or_away,
                    team,
                    game_prediction.opposition(team),
                    f"{sort_by_value:.3f}",
                    f"{custom_format_money(game_prediction.total_matched())}",
                    f"{game_prediction.total_overround():.3f}",
                    f"{game_prediction.score_more_than_two_probability_by_team(team):.3f}",
                    f"{game_prediction.clean_sheet_probability_by_team(team):.3f}",
                    f"{game_prediction.win_probability_by_team(team):.3f}",
                    f"{game_prediction.match_odds_win_probability_by_team(team):.3f}",
                    f"{game_prediction.total_goals_odds.line:.2f}",
                    f"{game_prediction.total_goals_odds.over.price:.3f}",
                    f"{game_prediction.total_goals_odds.under.price:.3f}",
                    f"{game_prediction.total_goals_odds.odds_ratio():.3f}",
                    f"{game_prediction.total_goals_odds.implied_probability_discrepancy():.3f}",
                    f"{custom_format_money(game_prediction.total_goals_odds.total_matched)}",
                    f"{game_prediction.asian_handicap_odds.home_line:.2f}",
                    f"{game_prediction.asian_handicap_odds.home_odds.price:.3f}",
                    f"{game_prediction.asian_handicap_odds.away_odds.price:.3f}",
                    f"{game_prediction.asian_handicap_odds.odds_ratio():.3f}",
                    f"{game_prediction.asian_handicap_odds.implied_probability_discrepancy():.3f}",
                    f"{custom_format_money(game_prediction.asian_handicap_odds.total_matched)}",
                    f"{game_prediction.match_odds.home.price:.3f}",
                    f"{game_prediction.match_odds.draw.price:.3f}",
                    f"{game_prediction.match_odds.away.price:.3f}",
                    f"{custom_format_money(game_prediction.match_odds.total_matched)}",
                    f"{game_prediction.expected_goals.home:.3f}",
                    f"{game_prediction.expected_goals.away:.3f}"
                ]))
        else:
            print(f"Login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def process_event(event):
    event_id = event['event']['id']
    event_name = event['event']['name']
    kickoff = kickoff_to_datetime(event['event']['openDate'])

    home_team_name, away_team_name = event_name.split(' v ')

    betfair_event = BetfairEvent(
        event_id=event_id,
        event_name=event_name,
        kickoff=kickoff,
        home_team=home_team_name,
        away_team=away_team_name,
    )

    # response = requests.post(list_competitions_endpoint, data=football_and_weekend_filter, headers=headers)
    # print(json.dumps(json.loads(response.text), indent=3))

    markets_for_a_game_filter = json.dumps({
        "filter": {
            "eventIds": [betfair_event.event_id],
            #"marketBettingTypes": ["ASIAN_HANDICAP_DOUBLE_LINE"],
        },
        "maxResults": 200,
        "marketProjection": [
            "RUNNER_DESCRIPTION",
            "RUNNER_METADATA"
        ]
    })
    list_market_catalogue_endpoint = url_prefix + 'listMarketCatalogue/'

    response = requests.post(list_market_catalogue_endpoint, data=markets_for_a_game_filter, headers=headers)
    #print(json.dumps(json.loads(response.text), indent=3))
    json_response = json.loads(response.text)
    markets = "\n".join([f"{market[MARKET_ID_KEY]},{market[MARKET_NAME_KEY]}" for market in json_response])
    #print(markets)
    print(f"{event_id}: {event_name}")

    match_odds = asian_handicap_odds = total_goals_odds = None

    for market in json_response:
        market_name = market[MARKET_NAME_KEY]
        if market_name == MATCH_ODDS_MARKET_NAME:
            match_odds = get_match_odds(market, home_team_name, away_team_name)
            print(match_odds)
        elif market_name == ASIAN_HANDICAP_MARKET_NAME:
            asian_handicap_odds = get_asian_handicap_odds(market)
            print(asian_handicap_odds)
        elif market_name == GOAL_LINE_MARKET_NAME:
            total_goals_odds = get_total_goals_odds(market)
            print(total_goals_odds)

    if match_odds is not None and asian_handicap_odds is not None and total_goals_odds is not None:
        expected_goals = find_expected_goals(match_odds, asian_handicap_odds, total_goals_odds)
        scoreline_probability_distribution = calculate_scoreline_distribution(expected_goals)

        expected_home_team_points = calculate_expected_home_team_points(scoreline_probability_distribution)
        expected_away_team_points = calculate_expected_away_team_points(scoreline_probability_distribution)

        return EFLGamePrediction(
            betfair_event=betfair_event,
            match_odds=match_odds,
            asian_handicap_odds=asian_handicap_odds,
            total_goals_odds=total_goals_odds,
            expected_goals=expected_goals,
            scoreline_probability_distribution=scoreline_probability_distribution,
            expected_home_points=expected_home_team_points,
            expected_away_points=expected_away_team_points
        )

    else:
        return None


def get_match_odds(market, home_team_name, away_team_name):
    match_odds_market_id = market[MARKET_ID_KEY]
    total_matched = Money(market[TOTAL_MATCHED_KEY], GBP)
    selections_by_id = {}

    for selection in market[RUNNERS_KEY]:
        selections_by_id[selection[SELECTION_ID_KEY]] = selection

    match_odds = market_book(match_odds_market_id)
    match_odds_result = MatchOdds(total_matched=total_matched)

    # print(json.dumps(match_odds, indent=3))

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


def get_asian_handicap_odds(market):
    asian_handicap_market_id = market[MARKET_ID_KEY]
    total_matched = Money(market[TOTAL_MATCHED_KEY], GBP)
    asian_handicap_odds = market_book(asian_handicap_market_id)

    asian_handicap_odds_result = AsianHandicapOdds(total_matched=total_matched)
    # print(json.dumps(asian_handicap_odds, indent=3))

    # Assumption that the primary handicap will be the first one in the keyLineDescription - will
    # be from the home team's point of view.
    home_primary_line_handicap = asian_handicap_odds[0][KEY_LINE_DESCRIPTION_KEY][KEY_LINE_KEY][0]
    home_primary_line_handicap_value = home_primary_line_handicap['handicap']

    away_primary_line_handicap = asian_handicap_odds[0][KEY_LINE_DESCRIPTION_KEY][KEY_LINE_KEY][1]
    away_primary_line_handicap_value = away_primary_line_handicap['handicap']

    asian_handicap_odds_result.home_line = home_primary_line_handicap_value
    asian_handicap_odds_result.away_line = away_primary_line_handicap_value

    for selection_book in asian_handicap_odds[0][RUNNERS_KEY]:
        # TODO: obvious duplication that can be fixed here but no need for now
        if (selection_book['handicap'] == home_primary_line_handicap_value and
                selection_book['selectionId'] == home_primary_line_handicap['selectionId']):
            best_back = selection_book['ex']['availableToBack'][0]['price']
            best_lay = selection_book['ex']['availableToLay'][0]['price']
            best_price = Odds((best_back + best_lay) / 2)

            asian_handicap_odds_result.home_odds = best_price
        elif (selection_book['handicap'] == away_primary_line_handicap_value and
                selection_book['selectionId'] == away_primary_line_handicap['selectionId']):
            best_back = selection_book['ex']['availableToBack'][0]['price']
            best_lay = selection_book['ex']['availableToLay'][0]['price']
            best_price = Odds((best_back + best_lay) / 2)

            asian_handicap_odds_result.away_odds = best_price

    return asian_handicap_odds_result


def get_total_goals_odds(market):
    total_goals_market_id = market[MARKET_ID_KEY]
    total_matched = Money(market[TOTAL_MATCHED_KEY], GBP)
    total_goals_market = market_book(total_goals_market_id)
    # print(json.dumps(total_goals_market, indent=3))
    primary_lines = total_goals_market[0][KEY_LINE_DESCRIPTION_KEY][KEY_LINE_KEY]

    total_goals_odds = TotalGoalsOdds(total_matched=total_matched)

    for selection in market[RUNNERS_KEY]:
        for primary_line in primary_lines:
            if (selection['selectionId'] == primary_line['selectionId'] and
                    selection['handicap'] == primary_line['handicap']):
                primary_line[RUNNER_NAME_KEY] = selection[RUNNER_NAME_KEY]
                break

    for primary_line in primary_lines:
        for selection_book in total_goals_market[0][RUNNERS_KEY]:
            if (selection_book['selectionId'] == primary_line['selectionId'] and
                    selection_book['handicap'] == primary_line['handicap']):
                total_goals_odds.line = primary_line['handicap']

                if (isinstance(selection_book['ex']['availableToBack'], list) and
                        len(selection_book['ex']['availableToBack']) > 0 and
                        isinstance(selection_book['ex']['availableToLay'], list) and
                        len(selection_book['ex']['availableToLay']) > 0):
                    best_back = selection_book['ex']['availableToBack'][0]['price']
                    best_lay = selection_book['ex']['availableToLay'][0]['price']
                    best_price = Odds((best_back + best_lay) / 2)

                    if primary_line[RUNNER_NAME_KEY] == 'Under':
                        total_goals_odds.under = best_price
                    else:
                        total_goals_odds.over = best_price
                    break
                else:
                    print("Back and lay not both available")
                    return None

    return total_goals_odds


def market_book(market_id):
    book_filter = json.dumps({
        "marketIds": [market_id],
        "priceProjection": {
            "priceData": ["EX_BEST_OFFERS"],
            "keyLineDescription": True
        }
    })
    list_market_book_endpoint = url_prefix + 'listMarketBook/'

    response = requests.post(list_market_book_endpoint, data=book_filter, headers=headers)
    return json.loads(response.text)


def kickoff_to_datetime(kickoff_string):
    naive_datetime_obj = datetime.strptime(kickoff_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return naive_datetime_obj.replace(tzinfo=timezone.utc)


def custom_format_money(money: Money):
    return f'{money.amount}'

main()
