from models import db, Team, Game, GameTeam
from datetime import datetime
import requests
import pytz
import json
import random
import time


def init_db():
    db.connect()
    db.create_tables([Team, Game, GameTeam])


def add_team(name):
    return Team.create(name=name)


def add_game(kickoff, team1, team2, home_goals=None, away_goals=None):
    game = Game.create(kickoff=kickoff)
    GameTeam.create(number=1, team=team1, game=game, full_time_score=home_goals)
    GameTeam.create(number=2, team=team2, game=game, full_time_score=away_goals)
    return game


def get_games():
    return Game.select().prefetch(GameTeam, Team)


def trim_name(name):
    return ''.join(name.split())


if __name__ == '__main__':
    init_db()

    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    teams = data['teams']
    players = data['elements']
    team_dictionary = {}

    for team_data in teams:
        id = team_data['id']
        team_name = team_data['name']
        team_dictionary[id] = add_team(team_name)

    url = 'https://fantasy.premierleague.com/api/fixtures/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    events = data

    for event in events:
        home_team = team_dictionary[event['team_h']]
        away_team = team_dictionary[event['team_a']]
        home_goals = event['team_h_score']
        away_goals = event['team_a_score']
        kickoff_string = event['kickoff_time']
        kickoff_object = datetime.strptime(kickoff_string, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
        add_game(kickoff_object, home_team, away_team, home_goals, away_goals)

    games = get_games()
    for game in games:
        home_team_result = game.home_team()
        away_team_result = game.away_team()
        print(f'Game @ {game.kickoff}: {home_team_result.team.name} v {away_team_result.team.name}: {home_team_result.full_time_score} : {away_team_result.full_time_score}')

    for player in players:
        code = player['code']
        player_id = player['id']
        first_name = player['first_name']
        second_name = player['second_name']
        display_name = player['web_name']
        player_url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            filename = \
                f'/data/{code}-{player_id}-{trim_name(first_name)}{trim_name(second_name)}-{trim_name(display_name)}.json'
            print(f"Writing {filename}")
            with open(filename, 'w') as file:
                json.dump(data, file)

            sleep_time = random.uniform(1, 4)
            print(f"Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)

