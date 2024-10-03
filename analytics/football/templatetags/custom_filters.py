from django import template
from typing import Dict

from football.league_table import LeagueTableRow, FixtureDifficulty

register = template.Library()

@register.filter
def get_fixture_difficulty_average_position(fixture_difficulties: Dict[LeagueTableRow, FixtureDifficulty],
                                            row: LeagueTableRow):
    return fixture_difficulties[row]
