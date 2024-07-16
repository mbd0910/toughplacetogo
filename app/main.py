from models import db, Team, Game, GameTeam
from datetime import datetime


def init_db():
    db.connect()
    db.create_tables([Team, Game, GameTeam])


def add_team(name):
    team = Team(name=name)
    team.save()
    return team


def add_game(kickoff, team1, team2):
    game = Game.create(kickoff=kickoff)
    GameTeam.create(number=1, team=team1, game=game)
    GameTeam.create(number=2, team=team2, game=game)
    return game


def get_teams():
    return Team.select()


def get_games():
    return Game.select().prefetch(GameTeam, Team)


if __name__ == '__main__':
    init_db()

    cafc = add_team('Charlton Athletic')
    notts = add_team('Notts County')

    game = add_game(datetime(year=2024, month=7, day=16, hour=15, minute=0, second=0), cafc, notts)

    teams = get_teams()
    for team in teams:
        print(f'Team {team.id}: {team.name}')

    games = get_games()
    for game in games:
        print(f'Game kicking off at {game.kickoff} between {game.home_team().name} and {game.away_team().name}')
