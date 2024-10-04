from django.core.management.base import BaseCommand

from football.models import Confederation, Country, Game, GameTeam, Team, TeamExternalLink, Stage
from football.enums import ExternalSource, Gender, TeamExternalLinkType, TeamType
import os
import csv
from datetime import datetime
from football.finder import CachingTeamFinder, find_game
import pytz


class Command(BaseCommand):
    help = 'Creates English games from downloaded football-data.co.uk spreadsheets'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='The full path to the directory to process')

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']
        caching_team_finder = CachingTeamFinder()

        for root, dirs, files in os.walk(directory):
            containing_folder = os.path.basename(root)
            for file in files:
                if file in ['E0.csv', 'E1.csv', 'E2.csv', 'E3.csv', 'EC.csv']:
                    season_name = containing_folder.replace(':', '/')
                    years = season_name.split('/')
                    if len(years) == 2:
                        start_year, end_year = years[0], years[1]
                        if int(start_year) >= 2019:
                            competition_name = self.competition_from_file_name(file)
                            stage = Stage.objects.get(
                                name='Regular Season',
                                season__name=season_name,
                                season__competition__name=competition_name,
                                season__competition__gender=Gender.MALE
                            )
                            file_path = os.path.join(root, file)
                            print(f"Processing file: {file_path}")
                            print(f"Stage {stage.name}, {stage.season.name}, {stage.season.competition.name}")
                            self.process_csv_file(file_path, stage, caching_team_finder)


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


    def process_csv_file(self, file_path, stage, caching_team_finder: CachingTeamFinder):
        with open(file_path, mode='r', newline='', encoding='Windows-1252') as csv_file:
            reader = csv.DictReader(csv_file)
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
                            stage=stage
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
