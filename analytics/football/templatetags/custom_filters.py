from django import template

from football.models import GameTeam

register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def game_team_metrics(game_team: GameTeam, source):
    for gtm in game_team.game_team_metrics.all():
        if gtm.source == source:
            return gtm
    return None
