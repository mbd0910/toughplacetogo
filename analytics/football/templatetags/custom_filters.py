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

@register.filter
def difficulty_colour(value):
    clamped_value = max(-3, min(value, 3))

    if clamped_value < 0:
        # For negative values (harder fixtures), increase red intensity
        red_intensity = (abs(clamped_value) / 3)  # Scale from 0 to 1
        green_intensity = 0
        alpha = red_intensity  # Fully opaque at -3, transparent at 0
    else:
        # For positive values (easier fixtures), increase green intensity
        green_intensity = (clamped_value / 3)  # Scale from 0 to 1
        red_intensity = 0
        alpha = green_intensity  # Fully opaque at +3, transparent at 0

    return f'rgba({int(red_intensity * 255)}, {int(green_intensity * 255)}, 0, {alpha})'

@register.filter()
def reverse_difficulty_colour(value):
    return difficulty_colour(-value)