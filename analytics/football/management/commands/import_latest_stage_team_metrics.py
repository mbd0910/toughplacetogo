from django.core.management.base import BaseCommand
from mobfot import MobFot

from football.finder import find_team
from football.enums import CompetitionExternalLinkType, ExternalSource, TeamExternalLinkType, Gender
from football.models import CompetitionExternalLink, StageTeamMetric, Stage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('competition_name', type=str, help='Competition name')

    def handle(self, *args, **kwargs):
        competition_name = kwargs['competition_name']
        season_name = '2024/2025'

        competition_external_link = CompetitionExternalLink.objects.get(
            competition__name=competition_name,
            source=ExternalSource.FOT_MOB,
            external_link_type=CompetitionExternalLinkType.ID
        )
        league_id = competition_external_link.value
        print(f'FotMob league ID for {competition_name} is {league_id}')
        stage = Stage.objects.get(
            name='Regular Season',
            season__name=season_name,
            season__competition__name=competition_name,
            season__competition__gender=Gender.MALE
        )

        client = MobFot()
        league_details = client.get_league(league_id)

        teams = league_details['table'][0]['data']['table']['xg']

        for team_xg_data in teams:
            fot_mob_team_id = team_xg_data['id']
            xg = team_xg_data['xg']
            xg_against = team_xg_data['xgConceded']
            x_points = team_xg_data['xPoints']
            points = team_xg_data['pts']

            team = find_team(fot_mob_team_id, TeamExternalLinkType.ID, ExternalSource.FOT_MOB)

            if team:
                print(f'Saving metrics for {team.name}')
                StageTeamMetric.objects.update_or_create(
                    stage=stage,
                    team=team,
                    source=ExternalSource.FOT_MOB,
                    defaults={
                        'xg': xg,
                        'xg_against': xg_against,
                        'x_points': x_points,
                        'points': points
                    }
                )
            else:
                print(f'Could not find team matching FotMob {team_xg_data['name']} ({fot_mob_team_id})')
