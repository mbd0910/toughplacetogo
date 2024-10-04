from datetime import datetime

from django.db.models import Count

from football.enums import ExternalSource
from football.models import Game, TeamExternalLink, TeamExternalLinkType, Team


def find_game(team1: Team, team2: Team, kickoff: datetime):
    date = kickoff.date()

    games = Game.objects.filter(
        kickoff__date=date,
        game_teams__team__in=[team1, team2]
    ).annotate(num_teams=Count('game_teams')).filter(num_teams=2).distinct()

    if len(games) == 1:
        return games[0]
    else:
        return None


def find_team(value: str,
              link_type: TeamExternalLinkType,
              source: ExternalSource):
    try:
        external_link = TeamExternalLink.objects.get(
            value=value,
            source=source,
            external_link_type=link_type
        )

        return external_link.team
    except Team.DoesNotExist:
        return None



class CachingTeamFinder:
    def __init__(self):
        self.cache = {}

    def find_team(self, value: str, link_type: TeamExternalLinkType, source: ExternalSource):
        key = self.key(value, link_type, source)

        if key not in self.cache:
            self.cache[key] = find_team(value, link_type, source)

        return self.cache[key]

    def key(self, value: str, link_type: TeamExternalLinkType, source: ExternalSource):
        return f"{value}:{link_type.value}:{source.value}"