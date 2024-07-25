from models import db, Team, Game, GameTeam, Competition, Season, Stage
import sys
import os
from datetime import datetime
import csv


def init_db():
    db.connect()
    db.create_tables([Team, Game, GameTeam, Competition, Season, Stage])


def parse_date(date_str):
    try:
        # Try parsing with four-digit year
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        # Fallback to two-digit year format if the four-digit format fails
        return datetime.strptime(date_str, "%d/%m/%y")


def empty_string_to_none(s):
    return None if s == "" else s


def process_csv_file(file_path, teams_by_name, stage):
    with open(file_path, mode='r', newline='', encoding='Windows-1252') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            home_team_name = row['HomeTeam']
            away_team_name = row['AwayTeam']
            ft_home_goals = row['FTHG']
            ft_away_goals = row['FTAG']
            ht_home_goals = empty_string_to_none(row['HTHG'])
            ht_away_goals = empty_string_to_none(row['HTAG'])
            date = row['Date']
            print(f"Raw data is {date}: {home_team_name} v {away_team_name} - {ft_home_goals} : {ft_away_goals}")

            kickoff = parse_date(date)

            game = Game.create(kickoff=kickoff, stage=stage)
            GameTeam.create(number=1, team=teams_by_name[home_team_name], game=game,
                            full_time_score=ft_home_goals, half_time_score=ht_home_goals)
            GameTeam.create(number=2, team=teams_by_name[away_team_name], game=game,
                            full_time_score=ft_away_goals, half_time_score=ht_away_goals)


def competition_from_file_name(file):
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


# Main function to traverse directories and process all CSV files
def main(directory, teams_by_name):
    for root, dirs, files in os.walk(directory):
        containing_folder = os.path.basename(root)
        for file in files:
            if file in ['E0.csv', 'E1.csv', 'E2.csv', 'E3.csv', 'EC.csv']:
                season_name = containing_folder.replace(':', '/')
                competition_name = competition_from_file_name(file)
                stage_query = (Stage.select()
                               .join(Season)
                               .join(Competition)
                               .where(
                                    Stage.name == 'Regular Season',
                                    Season.name == season_name,
                                    Competition.name == competition_name)
                               )
                stage = stage_query.get()
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                print(f"Stage {stage.name}, {stage.season.name}, {stage.season.competition.name}")
                process_csv_file(file_path, teams_by_name, stage)
                # Persist the games


directory_path = '/data/football-data/'


if __name__ == "__main__":
    init_db()

    persisted_teams = Team.select()
    teams_by_name = {}
    for team in persisted_teams:
        teams_by_name[team.name] = team

    main(directory_path, teams_by_name)

    # games = Game.select().prefetch(GameTeam, Team)
    # for game in games:
    #     home_team_result = game.home_team()
    #     away_team_result = game.away_team()
    #     print(f'Game @ {game.kickoff}: {home_team_result.team.name} v {away_team_result.team.name}: {home_team_result.full_time_score} : {away_team_result.full_time_score}')