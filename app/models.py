from datetime import datetime
from peewee import CharField, DateTimeField, PostgresqlDatabase, ForeignKeyField, IntegerField
from playhouse.signals import pre_save, Model
from config import DATABASE

db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)


class BaseModel(Model):
    class Meta:
        database = db


class TimestampableModel(BaseModel):
    created_at = DateTimeField()
    updated_at = DateTimeField()


class Team(TimestampableModel):
    name = CharField()


class Game(TimestampableModel):
    kickoff = DateTimeField()

    def home_team(self):
        return self.team(1)

    def away_team(self):
        return self.team(2)

    def team(self, number):
        for game_team in self.game_teams:
            if game_team.number == number:
                return game_team.team
        raise Exception(f'Cannot find game team with index {number}')


class GameTeam(TimestampableModel):
    number = IntegerField()
    team = ForeignKeyField(Team, backref='game_teams')
    game = ForeignKeyField(Game, backref='game_teams')


@pre_save(sender=TimestampableModel)
def on_save_handler(model_class, instance, created):
    if created:
        instance.created_at = datetime.now()
    instance.updated_at = datetime.now()
