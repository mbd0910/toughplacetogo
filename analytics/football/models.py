from django.db import models

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

TEAM_TYPE_CHOICES = [
    ('club', 'Club'),
    ('national', 'National')
]

COMPETITION_TYPE_CHOICES = [
    ('domestic', 'Club Domestic'),
    ('club_international', 'Club International'),
    ('national', 'National')
]

class Confederation(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'confederations'


class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=3, unique=True)
    confederation = models.ForeignKey(Confederation, on_delete=models.RESTRICT, related_name='countries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'countries'


class Venue(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='venues')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    what_3_words = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'venues'

        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='unique_venue_name_country')
        ]


class Team(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    team_type = models.CharField(max_length=20, choices=TEAM_TYPE_CHOICES)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='teams')
    league_country = models.ForeignKey(Country, on_delete=models.RESTRICT, null=True, related_name='league_teams')
    confederation = models.ForeignKey(Confederation, on_delete=models.RESTRICT, null=True, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='unique_team_name_country'),
            models.UniqueConstraint(fields=['code', 'country'], name='unique_team_code_country')
        ]


class Competition(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    competition_type = models.CharField(max_length=20, choices=COMPETITION_TYPE_CHOICES)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, null=True, related_name='competitions')
    confederation = models.ForeignKey(Confederation, on_delete=models.RESTRICT, null=True, related_name='competitions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'competitions'

        constraints = [
            models.UniqueConstraint(fields=['name', 'gender', 'country'], name='unique_competition_name_gender_country')
        ]


class Season(models.Model):
    name = models.CharField(max_length=200)
    competition = models.ForeignKey(Competition, on_delete=models.RESTRICT, related_name='seasons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seasons'

        constraints = [
            models.UniqueConstraint(fields=['name', 'competition'], name='unique_season_name_competition')
        ]

    def __str__(self):
        return f"{self.competition.name} - {self.name}"


class Stage(models.Model):
    name = models.CharField(max_length=200)
    season = models.ForeignKey(Season, on_delete=models.RESTRICT, related_name='stages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stages'

        constraints = [
            models.UniqueConstraint(fields=['name', 'season'], name='unique_stage_name_season')
        ]

    def __str__(self):
        return f"{self.season} - {self.name}"


class Game(models.Model):
    name = models.CharField(max_length=200, null=True)
    kickoff = models.DateTimeField()
    stage = models.ForeignKey(Stage, on_delete=models.RESTRICT, related_name='games')
    venue = models.ForeignKey('Venue', null=True, on_delete=models.RESTRICT, related_name='games')
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

        constraints = [
            models.UniqueConstraint(fields=['number', 'game'], name='unique_number_game'),
            models.UniqueConstraint(fields=['game', 'team'], name='unique_game_team')
        ]


class Person(models.Model):
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.display_name()

    def display_name(self):
        # Method to get the display name based on preferences
        if self.nickname:
            return self.nickname
        elif self.surname:
            return self.surname
        else:
            return self.full_name

    def full_display_name(self):
        # Method to get the full display name in "Nickname (Full Name)" format
        if self.nickname:
            return f"{self.nickname} ({self.full_name})"
        else:
            return self.full_name

# class Player(Person):
#     manager = models.OneToOneField('Manager')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

class Manager(Person):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'managers'


# class GameTeamMetric(models.Model):
#     game_team = models.ForeignKey(GameTeam, on_delete=models.CASCADE, related_name='game_team_metrics')
#     metric_type = models.ForeignKey('MetricType', on_delete=models.RESTRICT, related_name='game_team_metrics')
#     value = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'game_metrics'
#
#
# class MetricType(models.Model):
#     name = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'metric_types'