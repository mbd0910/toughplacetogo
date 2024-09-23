from django.core.management.base import BaseCommand

from football.models import Competition, Confederation, Country, Season, Stage
from football.enums import Gender, CompetitionType

class Command(BaseCommand):
    help = 'Creates English teams from downloaded football-data.co.uk spreadsheets'

    def handle(self, *args, **kwargs):
        season_names = [
            # '2003/2004',
            # '2004/2005',
            # '2005/2006',
            # '2006/2007',
            # '2007/2008',
            # '2008/2009',
            # '2009/2010',
            # '2010/2011',
            # '2011/2012',
            # '2012/2013',
            # '2013/2014',
            # '2014/2015',
            # '2015/2016',
            # '2016/2017',
            # '2017/2018',
            # '2018/2019',
            '2019/2020',
            '2020/2021',
            '2021/2022',
            '2022/2023',
            '2023/2024',
            '2024/2025'
        ]

        regular_season_name = 'Regular Season'

        england = Country.objects.get(name='England')
        uefa = Confederation.objects.get(code='UEFA')

        premier_league = self.create_competition('Premier League', england, uefa)
        championship = self.create_competition('Championship', england, uefa)
        league_one = self.create_competition('League One', england, uefa)
        league_two = self.create_competition('League Two', england, uefa)
        national_league = self.create_competition('National League', england, uefa)

        for season_name in season_names:
            for competition in [premier_league, championship, league_one, league_two, national_league]:
                season = Season.objects.create(name=season_name, competition=competition)
                stage = Stage.objects.create(name=regular_season_name, season=season)

        # Not handling playoffs as yet

    def create_competition(self, name: str, country: Country, confederation: Confederation):
        return Competition.objects.create(
            name=name,
            gender=Gender.MALE,
            competition_type=CompetitionType.DOMESTIC,
            country=country,
            confederation =confederation
        )