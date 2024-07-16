from models import db, Team


def init_db():
    db.connect()
    db.create_tables([Team])


def add_team(name):
    team = Team(name=name)
    team.save()


def get_teams():
    return Team.select()


if __name__ == '__main__':
    init_db()

    add_team('Charlton Athletic')
    add_team('Notts County')

    # Fetching and displaying users
    teams = get_teams()
    for team in teams:
        print(f'Team {team.id}: {team.name}')
