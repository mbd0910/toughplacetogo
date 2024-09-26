from django.http import HttpResponse

from football.models import Stage, Game, GameTeam, Team
from football.league_table import GamePOV, LeagueTable
from django.db.models import Prefetch


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
    games = Game.objects.prefetch_related(game_teams_with_team_prefetch).filter(stage=stage)

    calculate_league_table(games)

    return HttpResponse(f"This is the league table page for {stage.id} {stage.name}, game count {len(games)}")


def calculate_league_table(games):
    league_table = LeagueTable()
    for game in games:
        home_game_team = game.home_team()
        away_game_team = game.away_team()
        home_team = home_game_team.team
        away_team = away_game_team.team
        home_team_row = league_table.get_team_row(home_team)
        away_team_row = league_table.get_team_row(away_team)
        home_goals = home_game_team.full_time_score
        away_goals = away_game_team.full_time_score

        home_game_pov = GamePOV(home_team, away_team, home_goals, away_goals, is_home=True)
        away_game_pov = GamePOV(away_team, home_team, away_goals, home_goals, is_home=False)

        home_team_row.add_game_pov(home_game_pov)
        away_team_row.add_game_pov(away_game_pov)

    print(league_table)



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