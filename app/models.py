from __future__ import annotations
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

    def __str__(self):
        return f"{self.name} ({self.id})"


class Game(TimestampableModel):
    kickoff = DateTimeField()

    def home_team(self) -> GameTeam:
        return self.team(1)

    def away_team(self) -> GameTeam:
        return self.team(2)

    def team(self, number) -> GameTeam:
        for game_team in self.game_teams:
            if game_team.number == number:
                return game_team
        raise Exception(f'Cannot find game team with index {number}')


class Competition(TimestampableModel):
    name = CharField()


class Season(TimestampableModel):
    name = CharField()
    competition = ForeignKeyField(Competition, backref='seasons')


class Stage(TimestampableModel):
    name = CharField()
    season = ForeignKeyField(Season, backref='stages')
    # Could consider a foreign key to the competition here, but not strictly necessary


class GameTeam(TimestampableModel):
    number = IntegerField()
    half_time_score = IntegerField(null=True)
    full_time_score = IntegerField(null=True)
    after_extra_time_score = IntegerField(null=True)
    team = ForeignKeyField(Team, backref='game_teams')
    game = ForeignKeyField(Game, backref='game_teams')


@pre_save(sender=TimestampableModel)
def on_save_handler(model_class, instance, created):
    if created:
        instance.created_at = datetime.utcnow()
    instance.updated_at = datetime.utcnow()
