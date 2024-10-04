import csv
import os
from csv import DictReader
from datetime import datetime
from sys import prefix

import pytz
import requests
from django.core.management.base import BaseCommand

from football.enums import ExternalSource, Gender, TeamExternalLinkType
from football.finder import CachingTeamFinder, find_game
from football.models import Game, GameTeam, Stage


class Command(BaseCommand):
    help = 'Creates English games by reading remote football-data.co.uk CSV files'

    # TODO: make this more flexible in future
    prefix = 'https://www.football-data.co.uk/mmz4281/2425/'
    file_names = [
        'E0.csv',
        'E1.csv',
        'E2.csv',
        'E3.csv',
        'EC.csv'
    ]
    season_name = '2024/2025'

    def handle(self, *args, **kwargs):
        caching_team_finder = CachingTeamFinder()

        for file_name in self.file_names:
            url = f'{self.prefix}{file_name}'
            self.stdout.write(f"Fetching CSV from {url}")
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

            # Read CSV content
            csv_content = response.content.decode('Windows-1252').splitlines()
            reader = csv.DictReader(csv_content)

            competition_name = self.competition_from_file_name(file_name)
            stage = Stage.objects.get(
                name='Regular Season',
                season__name=self.season_name,
                season__competition__name=competition_name,
                season__competition__gender=Gender.MALE
            )
            self.process_csv_file(reader, stage, caching_team_finder)


    def parse_date(self, date_str, time_str):
        datetime_str = f"{date_str} {time_str}"
        for format in ("%d/%m/%Y %H:%M", "%d/%m/%y %H:%M"):
            try:
                return datetime.strptime(datetime_str, format)
            except ValueError:
                continue
        raise ValueError(f"Date and time format not recognized: {datetime_str}")


    def empty_string_to_none(self, s):
        return None if s == "" else s


    def process_csv_file(self, reader: DictReader, stage, caching_team_finder: CachingTeamFinder):
        for row in reader:
            home_team_name = row['HomeTeam']
            away_team_name = row['AwayTeam']
            ft_home_goals = row['FTHG']
            ft_away_goals = row['FTAG']
            ht_home_goals = self.empty_string_to_none(row['HTHG'])
            ht_away_goals = self.empty_string_to_none(row['HTAG'])
            date = row['Date']
            time = row['Time']
            print(f"Raw data is {date}: {home_team_name} v {away_team_name} - {ft_home_goals} : {ft_away_goals}")

            london_tz = pytz.timezone('Europe/London')
            utc_tz = pytz.utc
            kickoff = self.parse_date(date, time)
            kickoff = london_tz.localize(kickoff)
            kickoff = kickoff.astimezone(utc_tz)

            home_team = caching_team_finder.find_team(home_team_name, TeamExternalLinkType.NAME, ExternalSource.FOOTBALL_DATA)
            away_team = caching_team_finder.find_team(away_team_name, TeamExternalLinkType.NAME, ExternalSource.FOOTBALL_DATA)
            if home_team is not None and away_team is not None:
                game = find_game(home_team, away_team, kickoff)

                if game is None:
                    print(f"Creating game {date}: {home_team_name} v {away_team_name} - {ft_home_goals} : {ft_away_goals}")
                    game = Game.objects.create(
                        name=f"{home_team_name} v {away_team_name}",
                        kickoff=kickoff,
                        stage=stage,
                        finished=True
                    )
                    GameTeam.objects.create(
                        number=1,
                        team=home_team,
                        game=game,
                        full_time_score=ft_home_goals,
                        half_time_score=ht_home_goals
                    )
                    GameTeam.objects.create(
                        number=2,
                        team=away_team,
                        game=game,
                        full_time_score=ft_away_goals,
                        half_time_score=ht_away_goals
                    )
                else:
                    print("Game already exists. Doing nothing for now.")
            else:
                print("Couldn't find both teams")


    def competition_from_file_name(self, file: str):
        match file:
            case 'E0.csv':
                return 'Premier League'
            case 'E1.csv':
                return 'Championship'
            case 'E2.csv':
                return 'League One'
            case 'E3.csv':
                return 'League Two'
            case 'EC.csv':
                return 'National League'
