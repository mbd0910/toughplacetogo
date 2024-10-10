from django.core.management.base import BaseCommand
from mobfot import MobFot

from football.enums import ExternalSource, TeamExternalLinkType
from football.finder import guess_team
from football.models import Team, TeamExternalLink


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('league_id', type=int, help='Fotmob league ID')

    def handle(self, *args, **kwargs):
        league_id = kwargs['league_id']

        client = MobFot()
        league_details = client.get_league(league_id)

        teams = league_details['table'][0]['data']['table']['all']

        for team in teams:
            fot_mob_team_id = team['id']
            fot_mob_team_name = team['name']
            fot_mob_short_name = team['shortName']

            team = guess_team(fot_mob_team_name)

            if team is None:
               team = guess_team(fot_mob_short_name)

            if team is None:
                print(f'No matching team for {fot_mob_team_name} or {fot_mob_short_name} ({fot_mob_team_id}. Skipping.')
            else:
                print(f'Found match for {fot_mob_team_name}/{fot_mob_short_name}: {team} ({team.id})')
                self.persist_external_team_link(team, fot_mob_team_id)



    def persist_external_team_link(self, team: Team, team_id):
        TeamExternalLink.objects.create(
            team=team,
            source=ExternalSource.FOT_MOB,
            external_link_type=TeamExternalLinkType.ID,
            value=team_id
        )
