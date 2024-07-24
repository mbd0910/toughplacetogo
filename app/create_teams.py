from models import db, Team, Game, GameTeam, Competition, Season, Stage
import sys
import os
import csv


def init_db():
    db.connect()
    db.create_tables([Team, Game, GameTeam, Competition, Season, Stage])


# Function to process each CSV file and extract data from a specific field
def process_csv_file(file_path, data_field):
    extracted_data = []
    with open(file_path, mode='r', newline='', encoding='Windows-1252') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if data_field in row:
                extracted_data.append(row[data_field])
            else:
                print(f"Field '{data_field}' not found in {file_path}")
    return extracted_data


# Main function to traverse directories and process all CSV files
def extract_team_names(directory):
    print("Start of main")
    all_team_names = {}
    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        print(f"Visiting directory: {root}")  # Debug print
        print(f"Subdirectories: {dirs}")      # Debug print
        print(f"Files: {files}")              # Debug print
        for file in files:
            if file in ['E0.csv', 'E1.csv', 'E2.csv', 'E3.csv', 'EC.csv']:
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                team_names = process_csv_file(file_path, 'HomeTeam')
                for team_name in team_names:
                    all_team_names[team_name] = team_name
    return all_team_names


def clean_and_sort_team_names(team_names):
    return sorted(list(filter(None, team_names)))


directory_path = '/data/football-data/'


if __name__ == "__main__":
    init_db()
    extracted_team_names = extract_team_names(directory_path)
    sorted_teams = clean_and_sort_team_names(extracted_team_names.keys())
    for team_name in sorted_teams:
        Team.create(name=team_name)




