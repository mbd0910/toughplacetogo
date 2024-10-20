from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        competition_names = [
            'Premier League',
            'Championship',
            'League One',
            'League Two',
        ]

        for competition_name in competition_names:
            call_command('import_latest_results', competition_name)
            call_command('import_latest_stage_team_metrics', competition_name)