from dateutil import parser, tz
from django.core.management.base import BaseCommand
from django.db import transaction
from mobfot import MobFot

from football.enums import GameExternalLinkType, CompetitionExternalLinkType, ExternalSource, TeamExternalLinkType, \
    Gender
from football.finder import find_game, find_team
from football.models import Game, GameTeam, CompetitionExternalLink, GameExternalLink, Stage


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
        matches = client.get_matches_by_league(league_id)
        all_matches = matches['allMatches']

        for match in all_matches:
            fot_mob_game_id = match['id']
            fot_mob_home_team_id = match['home']['id']
            fot_mob_away_team_id = match['away']['id']

            status = match['status']
            has_finished = status['finished'] == True
            kickoff_string = status['utcTime']
            kickoff = parser.parse(kickoff_string)

            if kickoff.tzinfo is None:
                kickoff = kickoff.replace(tzinfo=tz.UTC)
            else:
                kickoff = kickoff.astimezone(tz.UTC)

            home_team = find_team(fot_mob_home_team_id, TeamExternalLinkType.ID, ExternalSource.FOT_MOB)
            away_team = find_team(fot_mob_away_team_id, TeamExternalLinkType.ID, ExternalSource.FOT_MOB)

            game_external_link = GameExternalLink.objects.filter(
                source=ExternalSource.FOT_MOB,
                external_link_type=GameExternalLinkType.ID,
                value=fot_mob_game_id
            ).first()

            if has_finished:
                score_str = status['scoreStr']
                goals = score_str.split(' - ')
                ft_home_goals = goals[0]
                ft_away_goals = goals[1]
            else:
                ft_home_goals = None
                ft_away_goals = None

            if game_external_link is None:
                game = find_game(home_team, away_team, kickoff)

                if game is None:
                    print(f'Creating Game, GameTeams and GameExternal link for {home_team.name} v {away_team.name} ({fot_mob_game_id})')
                    game = Game.objects.create(
                        name=f"{home_team.name} v {away_team.name}",
                        kickoff=kickoff,
                        stage=stage,
                        finished=has_finished
                    )
                    GameTeam.objects.create(
                        number=1,
                        team=home_team,
                        game=game,
                        full_time_score=ft_home_goals
                    )
                    GameTeam.objects.create(
                        number=2,
                        team=away_team,
                        game=game,
                        full_time_score=ft_away_goals
                    )
                    GameExternalLink.objects.create(
                        game=game,
                        source=ExternalSource.FOT_MOB,
                        external_link_type=GameExternalLinkType.ID,
                        value=fot_mob_game_id
                    )
                    continue
                else:
                    print(f'Found Game via home team, away team and kickoff - creating GameExternal link for {home_team.name} v {away_team.name} ({fot_mob_game_id})')

                    GameExternalLink.objects.create(
                        game=game,
                        source=ExternalSource.FOT_MOB,
                        external_link_type=GameExternalLinkType.ID,
                        value=fot_mob_game_id
                    )
            else:
                print(f'Found game via team external link - {home_team.name} v {away_team.name} ({fot_mob_game_id})')
                game = game_external_link.game

            print(f'Updating game kickoff, finished flag and scoreline')
            game.kickoff = kickoff
            game.finished = has_finished
            with transaction.atomic():
                game.save()
                home_game_team = game.home_team()
                home_game_team.full_time_score = ft_home_goals
                home_game_team.save()
                home_game_team = game.away_team()
                home_game_team.full_time_score = ft_away_goals
                home_game_team.save()
