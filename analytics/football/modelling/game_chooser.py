from abc import ABC, abstractmethod

from football.league_table import LeagueTableRow

class GameChooser(ABC):
    @abstractmethod
    def choose_games(self, league_table_row: LeagueTableRow):
        pass

class FixturesChooser(GameChooser):
    def choose_games(self, league_table_row: LeagueTableRow):
        return league_table_row.fixtures

class ResultsChooser(GameChooser):
    def choose_games(self, league_table_row: LeagueTableRow):
        return league_table_row.results

class RecentFormChooser(GameChooser):
    def choose_games(self, league_table_row: LeagueTableRow):
        return league_table_row.most_recent_games(5)

class UpcomingGamesChooser(GameChooser):
    def choose_games(self, league_table_row: LeagueTableRow):
        return league_table_row.upcoming_games(5)