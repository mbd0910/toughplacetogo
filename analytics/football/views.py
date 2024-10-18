from typing import List, Dict

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from football.enums import ExternalSource
from football.forms import GameTeamMetricForm
from football.league_table import GamePOV, LeagueTable, LeagueTableRow, normalise_difficulties
from football.modelling.game_chooser import ResultsChooser, FixturesChooser, GameChooser
from football.modelling.strength_of_schedule_calculator import calculate_strength_of_schedule, team_rating
from football.models import Stage, StagePointsDeduction, Game, GameTeamMetric, Team


def index(request):
    return HttpResponse("Hello, world. You're at the analytics index.")


def metrics_management(request, competition_name, season_name):
    db_competition_name, db_season_name = convert_competition_and_season_names(competition_name, season_name)
    stage, games = get_games_for_stage(db_competition_name, db_season_name)
    context = metrics_management_context(games, competition_name, season_name)

    return render(request, 'game_team_metrics_management.html', context)


def game_view(request, game_id: int):
    game = get_object_or_404(Game, id=game_id)
    url_season_name = convert_season_name_from_db_to_url(game.stage.season.name)
    url_competition_name = convert_competition_name_from_db_to_url(game.stage.season.competition.name)
    home_team = game.home_team()
    away_team = game.away_team()

    try:
        home_team_metrics = home_team.game_team_metrics.get(source=ExternalSource.FOT_MOB)
    except GameTeamMetric.DoesNotExist:
        home_team_metrics = GameTeamMetric(game_team=home_team, source=ExternalSource.FOT_MOB)

    try:
        away_team_metrics = away_team.game_team_metrics.get(source=ExternalSource.FOT_MOB)
    except GameTeamMetric.DoesNotExist:
        away_team_metrics = GameTeamMetric(game_team=away_team, source=ExternalSource.FOT_MOB)

    if request.method == 'GET':
        home_form = GameTeamMetricForm(instance=home_team_metrics, prefix='home')
        away_form = GameTeamMetricForm(instance=away_team_metrics, prefix='away')

        return render(request, 'game_view.html', {
            'game': game,
            'home_form': home_form,
            'away_form': away_form,
            'season_name': url_season_name,
            'competition_name': url_competition_name
        })
    elif request.method == 'POST':
        home_form = GameTeamMetricForm(request.POST, instance=home_team_metrics, prefix='home')
        away_form = GameTeamMetricForm(request.POST, instance=away_team_metrics, prefix='away')

        if home_form.is_valid() and away_form.is_valid():
            home_form.save()
            away_form.save()
            return redirect(f'/football/game/{game_id}')
        else:
            return render(request, 'game_view.html', {
                'game': game,
                'home_form': home_form,
                'away_form': away_form,
                'season_name': url_season_name,
                'competition_name': url_competition_name
            })


def league_table(request, competition_name, season_name):
    db_competition_name, db_season_name = convert_competition_and_season_names(competition_name, season_name)
    stage, games = get_games_for_stage(db_competition_name, db_season_name)
    context = calculate_contextual_league_table(stage, games, competition_name, season_name)

    return render(request, 'league_table.html', context)


def calculate_contextual_league_table(stage, games, competition_name, season_name):
    rows_by_team = {}

    points_deductions = StagePointsDeduction.objects.filter(stage=stage)
    points_deduction_by_team = { points_deduction.team: points_deduction.deduction for points_deduction in points_deductions }

    def get_league_table_row(team):
        if team not in rows_by_team:
            points_deduction = points_deduction_by_team[team] if team in points_deduction_by_team else 0
            rows_by_team[team] = LeagueTableRow(team=team, points_deduction=points_deduction)
        return rows_by_team[team]

    for game in games:
        home_game_team = game.home_team()
        away_game_team = game.away_team()
        home_team = home_game_team.team
        away_team = away_game_team.team

        home_team_row = get_league_table_row(home_team)
        away_team_row = get_league_table_row(away_team)
        home_goals = home_game_team.full_time_score
        away_goals = away_game_team.full_time_score

        home_game_pov = GamePOV(home_team, away_team, is_home=True, scored=home_goals, conceded=away_goals)
        away_game_pov = GamePOV(away_team, home_team, is_home=False, scored=away_goals, conceded=home_goals)

        if game.finished:
            home_team_row.add_result(home_game_pov)
            away_team_row.add_result(away_game_pov)
        else:
            home_team_row.add_fixture(home_game_pov)
            away_team_row.add_fixture(away_game_pov)

    for team_metrics in stage.team_metrics.all():
        team_row = get_league_table_row(team_metrics.team)
        team_row.xg = team_metrics.xg
        team_row.xg_against = team_metrics.xg_against
        team_row.x_points = team_metrics.x_points

    rows_sorted_by_points = sorted(
        rows_by_team.values(),
        key=lambda row: (row.points(), row.goal_difference(), row.scored, row.team.name),
        reverse=True
    )

    rows_sorted_by_performance_points = sorted(
        rows_by_team.values(),
        key=lambda row: (row.performance_points_per_game(), row.goal_difference(), row.scored, row.team.name),
        reverse=True
    )

    rows_sorted_by_x_points = sorted(
        rows_by_team.values(),
        key=lambda row: (row.x_points_per_game(), row.xg_difference()),
        reverse=True
    )

    traditional_league_table = LeagueTable(rows_sorted_by_points)
    strength_of_results_schedule = normalise_difficulties(calculate_strength_of_results_schedule(rows_by_team))
    strength_of_fixtures_schedule = normalise_difficulties(calculate_strength_of_fixtures_schedule(rows_by_team))
    team_ratings = calculate_team_ratings(rows_by_team)

    return {
        'league_table': traditional_league_table,
        'result_difficulties': {
            'sos': strength_of_results_schedule
        },
        'fixture_difficulties': {
            'sos': strength_of_fixtures_schedule
        },
        'competition_name': competition_name,
        'season_name': season_name,
        'team_ratings': team_ratings
    }

def calculate_strength_of_schedules(game_chooser: GameChooser, rows_by_team: Dict[Team, LeagueTableRow]) -> Dict[Team, float]:
    return {
        team: calculate_strength_of_schedule(team, game_chooser, rows_by_team)
        for team, row  in rows_by_team.items()
    }

def calculate_strength_of_results_schedule(rows_by_team: Dict[Team, LeagueTableRow]):
    return calculate_strength_of_schedules(ResultsChooser(), rows_by_team)

def calculate_strength_of_fixtures_schedule(rows_by_team: Dict[Team, LeagueTableRow]):
    return calculate_strength_of_schedules(FixturesChooser(), rows_by_team)

def calculate_team_ratings(rows_by_team: Dict[Team, LeagueTableRow]):
    return {
        team: team_rating(row)
        for team, row in rows_by_team.items()
    }

def metrics_management_context(games: List[Game], competition_name, season_name):
    unique_sources = {
        game_team_metric.source
        for game in games
        for game_team in game.game_teams.all()
        for game_team_metric in game_team.game_team_metrics.all()
    }

    unique_sources_list = list(unique_sources)

    return {
        'games': games,
        'competition_name': competition_name,
        'season_name': season_name,
        'unique_sources': unique_sources
    }


def convert_competition_and_season_names(competition_name, season_name):
    return convert_competition_name_from_url_to_db(competition_name), convert_season_name_from_url_to_db(season_name)

def convert_competition_name_from_url_to_db(competition_name):
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

def convert_competition_name_from_db_to_url(competition_name):
    return str.lower(competition_name).replace(' ', '-')

def convert_season_name_from_url_to_db(season_name):
    return str.replace(season_name, '-', '/')

def convert_season_name_from_db_to_url(season_name):
    return str.replace(season_name, '/', '-')

def get_games_for_stage(competition_name: str, season_name: str):
    stage = Stage.objects.get(
        season__name=season_name, season__competition__name=competition_name
    )

    games = Game.objects.filter(stage=stage).prefetch_related(
        'game_teams__team', 'game_teams__game_team_metrics'
    ).order_by('kickoff')

    return stage, games