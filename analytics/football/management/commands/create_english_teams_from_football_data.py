from django.core.management.base import BaseCommand

from football.models import Confederation, Country, Team, TeamExternalLink
from football.enums import ExternalSource, Gender, TeamExternalLinkType, TeamType
import os
import csv


class Command(BaseCommand):
    help = 'Creates English teams from downloaded football-data.co.uk spreadsheets'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='The full path to the directory to process')

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        extracted_team_names = self.extract_team_names(directory)
        sorted_teams = self.clean_and_sort_team_names(extracted_team_names.keys())
        print(sorted_teams)
        england = Country.objects.get(name='England')
        uefa = Confederation.objects.get(code='UEFA')

        for team_name in sorted_teams:
            team = Team.objects.create(
                name=team_name,
                country=england,
                league_country=england,
                confederation=uefa,
                gender=Gender.MALE,
                team_type=TeamType.CLUB
            )

            TeamExternalLink.objects.create(
                team=team,
                source=ExternalSource.FOOTBALL_DATA,
                external_link_type=TeamExternalLinkType.NAME,
                value=team_name
            )

    def extract_team_names(self, directory):
        print("Start of main")
        all_team_names = {}
        # Traverse the directory and its subdirectories
        for root, dirs, files in os.walk(directory):
            print(f"Visiting directory: {root}")
            dir_name = os.path.basename(root)
            years = dir_name.split(':')
            if len(years) == 2:
                start_year, end_year = years[0], years[1]
                if int(start_year) >= 2014:
                    print(f"Directory name: {dir_name}")
                    print(f"Files: {files}")
                    for file in files:
                        if file in ['E0.csv', 'E1.csv', 'E2.csv', 'E3.csv', 'EC.csv']:
                            file_path = os.path.join(root, file)
                            print(f"Processing file: {file_path}")
                            team_names = self.process_csv_file(file_path, 'HomeTeam')
                            for team_name in team_names:
                                all_team_names[team_name] = team_name
                else:
                    print(f"Skipping {dir_name}")
        return all_team_names

    def process_csv_file(self, file_path, data_field):
        extracted_data = []
        with open(file_path, mode='r', newline='', encoding='Windows-1252') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if data_field in row:
                    extracted_data.append(row[data_field])
                else:
                    print(f"Field '{data_field}' not found in {file_path}")
        return extracted_data

    def clean_and_sort_team_names(self, team_names):
        return sorted(list(filter(None, team_names)))