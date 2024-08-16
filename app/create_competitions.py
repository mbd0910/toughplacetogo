from models import db, Team, Game, GameTeam, Competition, Season, Stage
import sys
import os
from datetime import datetime
import csv


def init_db():
    db.connect()
    db.create_tables([Team, Game, GameTeam, Competition, Season, Stage])


if __name__ == "__main__":
    init_db()

    competitions = [
        'Premier League',
        'Championship',
        'League One',
        'League Two',
        'National League'
    ]

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
        '2014/2015',
        '2015/2016',
        '2016/2017',
        '2017/2018',
        '2018/2019',
        '2019/2020',
        '2020/2021',
        '2021/2022',
        '2022/2023',
        '2023/2024',
        '2024/2025'
    ]

    stage_name = 'Regular Season'

    premier_league = Competition.create(name='Premier League')
    championship = Competition.create(name='Championship')
    league_one = Competition.create(name='League One')
    league_two = Competition.create(name='League Two')
    national_league = Competition.create(name='National League')

    for season_name in season_names:
        for competition in [premier_league, championship, league_one, league_two, national_league]:
            season = Season.create(name=season_name, competition=competition)
            stage = Stage.create(name=stage_name, season=season)
