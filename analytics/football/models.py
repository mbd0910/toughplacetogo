from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'countries'


class Team(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'


class Competition(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'competitions'


class Season(models.Model):
    name = models.CharField(max_length=200)
    competition = models.ForeignKey(Competition, on_delete=models.RESTRICT, related_name='seasons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seasons'

    def __str__(self):
        return f"{self.competition.name} - {self.name}"


class Stage(models.Model):
    name = models.CharField(max_length=200)
    season = models.ForeignKey(Season, on_delete=models.RESTRICT, related_name='stages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stages'

    def __str__(self):
        return f"{self.season} - {self.name}"


class Game(models.Model):
    name = models.CharField(max_length=200, null=True)
    kickoff = models.DateTimeField()
    stage = models.ForeignKey(Stage, on_delete=models.RESTRICT, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'games'


class GameTeam(models.Model):
    number = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_teams')
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name='game_teams')
    half_time_score = models.IntegerField(null=True)
    full_time_score = models.IntegerField(null=True)
    after_extra_time_score = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'game_teams'


class GameTeamMetric(models.Model):
    game_team = models.ForeignKey(GameTeam, on_delete=models.CASCADE, related_name='game_team_metrics')
    metric_type = models.ForeignKey('MetricType', on_delete=models.RESTRICT, related_name='game_team_metrics')
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'game_metrics'


class MetricType(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'metric_types'
