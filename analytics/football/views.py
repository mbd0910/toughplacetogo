from datetime import datetime

from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render

from football.league_table import GamePOV, LeagueTable, LeagueTableRow, calculate_fixture_difficulties
from football.models import Stage, Game, GameTeam


def index(request):
    return HttpResponse("Hello, world. You're at the analytics index.")


def league_table(request, competition_name, season_name):
    competition_name = convert_competition_name(competition_name)
    season_name = convert_season_name(season_name)

    stage = Stage.objects.get(season__name=season_name, season__competition__name=competition_name)

    game_teams_with_team_prefetch = Prefetch(
        'game_teams',
        queryset=GameTeam.objects.select_related('team'),
    )
    games = Game.objects.prefetch_related(game_teams_with_team_prefetch).filter(stage=stage).order_by('kickoff')

    context = calculate_league_table(games)

    return render(request, 'league_table.html', context)


def calculate_league_table(games):
    rows_by_team_name = {}

    def get_league_table_row(team):
        team_name = team.name
        if team_name not in rows_by_team_name:
            rows_by_team_name[team_name] = LeagueTableRow(team)
        return rows_by_team_name[team_name]

    for game in games:
        home_game_team = game.home_team()
        away_game_team = game.away_team()
        home_team = home_game_team.team
        away_team = away_game_team.team

        home_team_row = get_league_table_row(home_team)
        away_team_row = get_league_table_row(away_team)
        home_goals = home_game_team.full_time_score
        away_goals = away_game_team.full_time_score

        home_game_pov = GamePOV(home_team, away_team, home_goals, away_goals, is_home=True)
        away_game_pov = GamePOV(away_team, home_team, away_goals, home_goals, is_home=False)

        home_team_row.add_game_pov(home_game_pov)
        away_team_row.add_game_pov(away_game_pov)

    sorted_league_table_rows = sorted(
        rows_by_team_name.values(),
        key=lambda row: (row.points(), row.goal_difference(), row.scored, row.team.name),
        reverse=True
    )

    league_table = LeagueTable(sorted_league_table_rows)
    fixture_difficulties = calculate_fixture_difficulties(league_table)

    return {
        'league_table': league_table,
        'fixture_difficulties': fixture_difficulties
    }



def convert_competition_name(competition_name):
    match competition_name:
        case 'premier-league':
            return 'Premier League'
        case 'championship':
            return 'Championship'
        case 'league-one':
            return 'League One'
        case 'league-two':
            return 'League Two'
        case _:
            raise NotImplementedError(f'Unknown competition {competition_name}')

def convert_season_name(season_name):
    return str.replace(season_name, '-', '/')