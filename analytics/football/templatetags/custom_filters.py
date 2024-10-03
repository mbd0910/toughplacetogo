from django import template

register = template.Library()

@register.filter
def get_fixture_difficulty_average_position(fixture_difficulties, team_name):
    return fixture_difficulties[team_name].average_position
